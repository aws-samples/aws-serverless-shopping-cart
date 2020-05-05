import json
import logging
import os

import boto3
from aws_xray_sdk.core import patch
from boto3.dynamodb.conditions import Key
from shared import handle_decimal_type, get_user_sub, get_cart_id, get_headers

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

    cart_id, generated = get_cart_id(event["headers"])

    # Because this method can be called anonymously, we need to check there's a logged in user
    jwt_token = event["headers"].get("Authorization")
    if jwt_token:
        user_sub = get_user_sub(jwt_token)
        key_string = f"user#{user_sub}"
    else:
        key_string = f"cart#{cart_id}"

    # No need to query database if the cart_id was generated rather than passed into the function
    if generated:
        product_list = []
    else:
        # Get a list of all the products in the cart
        response = table.query(
            KeyConditionExpression=Key("pk").eq(key_string)
            & Key("sk").begins_with("product#"),
            ProjectionExpression="sk,quantity,productDetail",
            FilterExpression="quantity > :val",  # Only return items with more than 0 quantity
            ExpressionAttributeValues={":val": 0},
        )
        product_list = response.get("Items", [])

    for product in product_list:
        product.update(
            (k, v.replace("product#", "")) for k, v in product.items() if k == "sk"
        )

    return {
        "statusCode": 200,
        "headers": get_headers(cart_id),
        "body": json.dumps({"products": product_list}, default=handle_decimal_type),
    }
