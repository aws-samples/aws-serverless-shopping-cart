import json
import logging
import os

import boto3
from aws_xray_sdk.core import patch
from shared import handle_decimal_type

libraries = ("boto3",)
patch(libraries)
logger = logging.getLogger()
logger.setLevel(os.environ["LOG_LEVEL"])

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    List items in shopping cart.
    """
    logger.debug(event)

    product_id = event["pathParameters"]["product_id"]
    response = table.get_item(Key={"pk": f"product#{product_id}", "sk": "totalquantity"})
    quantity = response['Item']['quantity']

    return {
        "statusCode": 200,
        "body": json.dumps({"product": product_id, "quantity": quantity}, default=handle_decimal_type),
    }
