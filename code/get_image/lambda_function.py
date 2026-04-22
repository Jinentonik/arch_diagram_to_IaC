import json
import boto3
from urllib.parse import urlparse
import base64
import os 

def download_file_from_s3(s3_uri, local_dir):
    
    """
    Download a file from an S3 bucket to a local directory.

    :param s3_uri: str, S3 URI of the file (e.g., 's3://bucket_name/key_name')
    :param local_dir: str, Local directory path where the file will be saved
    :return: str, Local file path of the downloaded file
    
    """
    
    try:
        # Parse the S3 URI
        parsed_url = urlparse(s3_uri)
        bucket_name = parsed_url.netloc
        key_name = parsed_url.path.lstrip('/')
        print('bucket name', bucket_name)
        print('key name', key_name)
        # Create a boto3 client
        s3_client = boto3.client('s3')

        # Ensure the local directory exists
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        # Define the local file path
        local_file_path = os.path.join(local_dir, os.path.basename(key_name))

        # Download the file from S3
        s3_client.download_file(bucket_name, key_name, local_file_path)
        print("File downloaded")

        return local_file_path

    except Exception as e:
        
        print(f"Error downloading file from S3: {e}")
        return None

def get_image_data(image_file):
    
    with open(image_file, "rb") as imagefile:
        image_data = base64.b64encode(imagefile.read()).decode("utf-8")
        print("Image data generated")
        
    return image_data

def lambda_handler(event, context):
    # TODO implement
    image_s3_uri = event['file_path']
    #code_language = event['code_language']
    #connection_id = event.get('connection_id')  # Optional connection ID for targeted WebSocket messages
    image_path = download_file_from_s3(image_s3_uri, "/tmp")
    print('image path', image_path)
    encoded_image= get_image_data(image_path)
    
    return {
        'statusCode': 200,
        'encoded_image': encoded_image
    }
