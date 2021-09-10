import json
import os
import threading

import boto3
from boto3.dynamodb.conditions import Key

from shared import generate_ttl, get_cart_id, get_headers, handle_decimal_type

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
sqs = boto3.resource("sqs")
queue = sqs.Queue(os.environ["DELETE_FROM_CART_SQS_QUEUE"])


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

    # Get all cart items belonging to the user's anonymous identity
    response = table.query(
        KeyConditionExpression=Key("pk").eq(f"cart#{cart_id}")
        & Key("sk").begins_with("product#")
    )
    unauth_cart = response["Items"]

    # Since there's no batch operation available for updating items, and there's no dependency between them, we can
    # run them in parallel threads.
    thread_list = []

    for item in unauth_cart:
        # Store items with user identifier as pk instead of "unauthenticated" cart ID
        # Using threading library to perform updates in parallel
        ddb_updateitem_thread = threading.Thread(
            target=update_item, args=(user_id, item)
        )
        thread_list.append(ddb_updateitem_thread)
        ddb_updateitem_thread.start()

        # Delete items with unauthenticated cart ID
        # Rather than deleting directly, push to SQS queue to handle asynchronously
        queue.send_message(MessageBody=json.dumps(item, default=handle_decimal_type))

    for ddb_thread in thread_list:
        ddb_thread.join()  # Block main thread until all updates finished

    response = table.query(
        KeyConditionExpression=Key("pk").eq(f"user#{user_id}")
        & Key("sk").begins_with("product#"),
        ProjectionExpression="sk,quantity,productDetail",
        ConsistentRead=True,  # Perform a strongly consistent read here to ensure we get correct values after updates
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
