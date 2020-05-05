import json
import logging
import os

import boto3
from aws_xray_sdk.core import patch

libraries = ("boto3",)
patch(libraries)

logger = logging.getLogger()
logger.setLevel(os.environ["LOG_LEVEL"])

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Handle messages from SQS Queue containing cart items, and delete them from DynamoDB.
    """
    logger.debug(event)

    records = event["Records"]

    with table.batch_writer() as batch:
        for item in records:
            item_body = json.loads(item["body"])
            batch.delete_item(Key={"pk": item_body["pk"], "sk": item_body["sk"]})

    return {
        "statusCode": 200,
    }
