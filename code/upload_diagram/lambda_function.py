import json
import boto3
import uuid
from datetime import datetime
from botocore.config import Config

s3 = boto3.client(
    "s3",
    config=Config(
        signature_version="s3v4",
        s3={"payload_signing_enabled": False}
    )
)

dynamodb = boto3.resource("dynamodb")

TABLE = dynamodb.Table("tf-diagram-to-terraform-jobs")
BUCKET = "diagram-to-terraform-input"

def lambda_handler(event, context):
    try:
        print(event)
        body = json.loads(event["body"])
        job_id = str(uuid.uuid4())

        key = f"uploads/{job_id}/{body['fileName']}"

        TABLE.put_item(
            Item={
                "jobId": job_id,
                "status": "UPLOADED",
                "progress": 10,
                "inputBucket": BUCKET,
                "inputKey": key,
                "createdAt": datetime.utcnow().isoformat()
            }
        )

        url = s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": BUCKET, "Key": key},
            ExpiresIn=900
        )

        return {
            "statusCode": 200,
            "headers": { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"      
            },
            "body": json.dumps({
                "jobId": job_id,
                "uploadUrl": url
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"      
            },
            "body": json.dumps({
                "error": str(e)
            })
        }