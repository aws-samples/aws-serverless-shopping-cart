import json
import os

import boto3
from aws_lambda_powertools import Logger, Tracer

from shared import handle_decimal_type

logger = Logger()
tracer = Tracer()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    List items in shopping cart.
    """
    product_id = event["pathParameters"]["product_id"]
    response = table.get_item(
        Key={"pk": f"product#{product_id}", "sk": "totalquantity"}
    )
    quantity = response["Item"]["quantity"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"product": product_id, "quantity": quantity}, default=handle_decimal_type
        ),
    }
