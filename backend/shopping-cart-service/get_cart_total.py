import json
import os

import boto3

from shared import handle_decimal_type


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


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
