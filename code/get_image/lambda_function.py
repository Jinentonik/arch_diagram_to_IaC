import boto3
import base64
import os 
import json

def download_file_from_s3(bucket_name, key_name, local_dir):
    
    """
    Download a file from an S3 bucket to a local directory.

    :param s3_uri: str, S3 URI of the file (e.g., 's3://bucket_name/key_name')
    :param local_dir: str, Local directory path where the file will be saved
    :return: str, Local file path of the downloaded file
    
    """
    
    try:
        # Parse the S3 URI
        
        print("Bucket:", bucket_name)
        print("Key:", key_name)

        # Create a boto3 client
        s3_client = boto3.client('s3')

        # Ensure the local directory exists
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        # Define the local file path
        local_file_path = os.path.join(local_dir, os.path.basename(key_name))

        # Download the file from S3
        s3_client.download_file(bucket_name, key_name, local_file_path)
        print("File downloaded to", local_file_path)

        return local_file_path

    except Exception as e:
        
        print(f"Error downloading file from S3: {e}")
        return None

def get_image_data(image_file):
    
    with open(image_file, "rb") as imagefile:
        image_data = base64.b64encode(imagefile.read()).decode("utf-8")
        print("Image data generated")
        
    return image_data


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
    # TODO implement

    try:
        print(event)
        # ✅ Extract bucket and key from EventBridge event
        bucket_name = event.get('bucket')
        key_name = event.get('objectKey')

        
        # ✅ Derive jobId from key path: uploads/{jobId}/filename
        job_id = key_name.split("/")[1]
        print("Job ID:", job_id)
        
        # ✅ Download image
        image_path = download_file_from_s3(
            bucket_name=bucket_name,
            key_name=key_name,
            local_dir="/tmp"
        )

        
        # ✅ Convert image to base64
        encoded_image = get_image_data(image_path)
        # update job status
        
        update_job(
            job_id=job_id,
            status="RETRIEVE_UPLOADED_IMAGE",
            progress=20
        )

        # ✅ Return structured output for Step Function
        return {
            "statusCode": 200,
            "jobId": job_id,
            "bucket": bucket_name,
            "key": key_name,
            "encoded_image": encoded_image
        }

    except Exception as e:
        print("Lambda failure:", str(e))
        return {
            "statusCode": 500,
            "error": str(e)
        }
