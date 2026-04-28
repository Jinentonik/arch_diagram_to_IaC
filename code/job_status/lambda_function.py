import json
import boto3

dynamodb = boto3.resource("dynamodb")
TABLE = dynamodb.Table("diagram-to-terraform-jobs")

def handler(event, context):
    job_id = event["queryStringParameters"]["jobId"]

    resp = TABLE.get_item(Key={"jobId": job_id})
    item = resp["Item"]

    body = {
        "status": item["status"],
        "progress": item["progress"]
    }

    if item["status"] == "COMPLETED":
        body["downloadUrl"] = item["downloadUrl"]

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps(body)
    }