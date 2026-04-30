import boto3
import os
import zipfile
from urllib.parse import urlparse
from datetime import datetime
import json

s3 = boto3.client("s3")

TMP_DIR = "/tmp"



def parse_s3_uri(s3_uri: str):
    parsed = urlparse(s3_uri)
    if parsed.scheme != "s3":
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    return parsed.netloc, parsed.path.lstrip("/")

def update_job(job_id, status, progress, download_url=None, error_message=None):
    lambda_client = boto3.client("lambda")
    update_job_lambda_arn = os.getenv('UPDATE_JOB_LAMBDA_ARN')
    payload = {
        "jobId": job_id,
        "status": status,
        "progress": progress
    }

    if download_url:
        payload["downloadUrl"] = download_url

    if error_message:
        payload["errorMessage"] = error_message

    lambda_client.invoke(
        FunctionName=update_job_lambda_arn,
        InvocationType="Event",
        Payload=json.dumps(payload).encode("utf-8")
    )

def lambda_handler(event, context):
    
    """
    Zips multiple S3 objects into a single archive folder and returns a presigned URL.
    """

    print(event)

    # Event is a list of objects
    if not isinstance(event, list) or len(event) == 0:
        raise ValueError("Event must be a non-empty list")

    job_id = event[0]["jobId"]

    source_s3_uris = [item["source_s3_uris"] for item in event]

    destination_bucket = os.getenv("S3_CODE_BUCKET")
    destination_prefix = "generated_code"
    zip_folder_name = "files"
    presign_expiration = 3600

    zip_filename = "combined-files.zip"
    local_zip_path = os.path.join(TMP_DIR, zip_filename)

    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d")
    destination_key = f"{destination_prefix}/{now_str}/{job_id}/{zip_filename}"

    with zipfile.ZipFile(local_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for s3_uri in source_s3_uris:
            bucket, key = parse_s3_uri(s3_uri)
            filename = os.path.basename(key)

            local_file_path = os.path.join(TMP_DIR, filename)
            s3.download_file(bucket, key, local_file_path)

            zipf.write(local_file_path, arcname=f"{zip_folder_name}/{filename}")
            os.remove(local_file_path)

    s3.upload_file(local_zip_path, destination_bucket, destination_key)

    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": destination_bucket, "Key": destination_key},
        ExpiresIn=presign_expiration,
    )

    update_job(
        job_id=job_id,
        status="COMPLETED",
        progress=100,
        download_url=presigned_url,
    )

    return {
        "statusCode": 200,
        "zip_s3_path": f"s3://{destination_bucket}/{destination_key}",
        "file_count": len(source_s3_uris),
        "presigned_url": presigned_url,
        "expires_in_seconds": presign_expiration,
        "jobId": job_id,
    }

