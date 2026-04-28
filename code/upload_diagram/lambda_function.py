import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE = dynamodb.Table("diagram-to-terraform-jobs")
BUCKET = "diagram-to-terraform-input"

def handler(event, context):
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
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps({
            "jobId": job_id,
            "uploadUrl": url
        })
    }