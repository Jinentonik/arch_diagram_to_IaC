import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import os

dynamodb = boto3.resource("dynamodb")
ddb_table_name = os.getenv("DDB_TABLE_NAME")
table = dynamodb.Table(ddb_table_name)

def lambda_handler(event, context):
    """
    Expected payload:
    {
      "jobId": "uuid",
      "status": "GENERATING_TERRAFORM",
      "progress": 85,
      "downloadUrl": "https://...",        # optional
      "errorMessage": "error details"      # optional
    }
    """
    print(event)
    job_id = event["jobId"]
    status = event["status"]
    progress = int(event["progress"])
    download_url = event.get("downloadUrl")
    error_message = event.get("errorMessage")

    update_expr = []
    expr_names = {}
    expr_values = {}

    update_expr.append("#status = :status")
    update_expr.append("#progress = :progress")
    update_expr.append("#updatedAt = :updatedAt")

    expr_names["#status"] = "status"
    expr_names["#progress"] = "progress"
    expr_names["#updatedAt"] = "updatedAt"

    expr_values[":status"] = status
    expr_values[":progress"] = progress
    expr_values[":updatedAt"] = datetime.utcnow().isoformat()

    if download_url:
        update_expr.append("#downloadUrl = :downloadUrl")
        expr_names["#downloadUrl"] = "downloadUrl"
        expr_values[":downloadUrl"] = download_url

    if error_message:
        update_expr.append("#errorMessage = :errorMessage")
        expr_names["#errorMessage"] = "errorMessage"
        expr_values[":errorMessage"] = error_message

    try:
        table.update_item(
            Key={"jobId": job_id},
            UpdateExpression="SET " + ", ".join(update_expr),
            ConditionExpression="attribute_not_exists(#progress) OR #progress <= :progress",
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values
        )

        return {
            "statusCode": 200,
            "message": f"Job {job_id} updated ({progress}%)"
        }

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "statusCode": 200,
                "message": "Ignored lower-progress update"
            }
        raise