import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Handle messages from SQS Queue containing cart items, and delete them from DynamoDB.
    """

    records = event["Records"]
    with table.batch_writer() as batch:
        for item in records:
            item_body = json.loads(item["body"])
            batch.delete_item(Key={"pk": item_body["pk"], "sk": item_body["sk"]})

    return {
        "statusCode": 200,
    }
