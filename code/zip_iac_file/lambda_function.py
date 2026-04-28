import boto3
import os
import zipfile
from urllib.parse import urlparse
from datetime import datetime

s3 = boto3.client("s3")

TMP_DIR = "/tmp"



def parse_s3_uri(s3_uri: str):
    parsed = urlparse(s3_uri)
    if parsed.scheme != "s3":
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def lambda_handler(event, context):
    """
    Zips multiple S3 objects into a single archive folder and returns a presigned URL.
    """
    

    source_s3_uris = event["source_s3_uris"]
    log_stream_id = event.get('log_stream')
    destination_bucket = "test-a2a-bucket"
    destination_prefix = f"generated_code"
    zip_folder_name = event.get("zip_folder_name", "files")
    presign_expiration = event.get("presign_expiration", 3600)

    if not source_s3_uris:
        raise ValueError("source_s3_uris must contain at least one S3 URI")

    zip_filename = "combined-files.zip"
    local_zip_path = os.path.join(TMP_DIR, zip_filename)
    now = datetime.now()
    now_str = now.strftime('%Y/%m/%d')
    destination_key = f"{destination_prefix}/{now_str}/{log_stream_id}/{zip_filename}"

    # Create zip file
    with zipfile.ZipFile(local_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for s3_uri in source_s3_uris:
            bucket, key = parse_s3_uri(s3_uri)
            filename = os.path.basename(key)

            local_file_path = os.path.join(TMP_DIR, filename)

            # Download each file
            s3.download_file(bucket, key, local_file_path)

            # Add to ZIP under a folder
            zip_path = f"{zip_folder_name}/{filename}"
            zipf.write(local_file_path, arcname=zip_path)

            # Cleanup file immediately to save space
            os.remove(local_file_path)

    # Upload ZIP to S3
    s3.upload_file(local_zip_path, destination_bucket, destination_key)

    # Generate presigned URL
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": destination_bucket,
            "Key": destination_key,
        },
        ExpiresIn=presign_expiration,
    )

    return {
        "statusCode": 200,
        "zip_s3_path": f"s3://{destination_bucket}/{destination_key}",
        "file_count": len(source_s3_uris),
        "presigned_url": presigned_url,
        "expires_in_seconds": presign_expiration,
    }
