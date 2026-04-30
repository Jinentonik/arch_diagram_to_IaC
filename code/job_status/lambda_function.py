import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
ddb_table_name = os.getenv('DDB_TABLE_NAME')
TABLE = dynamodb.Table(ddb_table_name)

def lambda_handler(event, context):
    print(event)
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
        "headers": { 
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body, default=str)
    }