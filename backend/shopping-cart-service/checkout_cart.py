import json
import logging
import os

import boto3
from aws_xray_sdk.core import patch
from boto3.dynamodb.conditions import Key
from shared import get_headers, generate_ttl, handle_decimal_type, get_cart_id

libraries = ("boto3",)
patch(libraries)

logger = logging.getLogger()
logger.setLevel(os.environ["LOG_LEVEL"])

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def update_item(user_id, item):
    """
    Update an item in the database, adding the quantity of the passed in item to the quantity of any products already
    existing in the cart.
    """
    table.update_item(
        Key={"pk": f"user#{user_id}", "sk": item["sk"]},
        ExpressionAttributeNames={
            "#quantity": "quantity",
            "#expirationTime": "expirationTime",
            "#productDetail": "productDetail",
        },
        ExpressionAttributeValues={
            ":val": item["quantity"],
            ":ttl": generate_ttl(days=30),
            ":productDetail": item["productDetail"],
        },
        UpdateExpression="ADD #quantity :val SET #expirationTime = :ttl, #productDetail = :productDetail",
    )


def lambda_handler(event, context):
    """
    Update cart table to use user identifier instead of anonymous cookie value as a key. This will be called when a user
    is logged in.
    """
    logger.debug(event)
    cart_id, _ = get_cart_id(event["headers"])

    try:
        # Because this method is authorized at API gateway layer, we don't need to validate the JWT claims here
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    except KeyError:

        return {
            "statusCode": 400,
            "headers": get_headers(cart_id),
            "body": json.dumps({"message": "Invalid user"}),
        }

    # Get all cart items belonging to the user's identity
    response = table.query(
        KeyConditionExpression=Key("pk").eq(f"user#{user_id}")
        & Key("sk").begins_with("product#"),
        ConsistentRead=True,  # Perform a strongly consistent read here to ensure we get correct and up to date cart
    )

    # batch_writer will be used to update status for cart entries belonging to the user
    with table.batch_writer() as batch:
        for item in response.get("Items"):
            # Delete ordered items
            batch.delete_item(Key={"pk": item["pk"], "sk": item["sk"]})

    # TODO: Notify another service that an order has been made

    return {
        "statusCode": 200,
        "headers": get_headers(cart_id),
        "body": json.dumps(
            {"products": response.get("Items")}, default=handle_decimal_type
        ),
    }
