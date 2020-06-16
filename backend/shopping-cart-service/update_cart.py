import json
import os

import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer

from shared import (
    NotFoundException,
    generate_ttl,
    get_cart_id,
    get_headers,
    get_user_sub,
)
from utils import get_product_from_external_service

logger = Logger()
tracer = Tracer()
metrics = Metrics()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
product_service_url = os.environ["PRODUCT_SERVICE_URL"]


@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    Idempotent update quantity of products in a cart. Quantity provided will overwrite existing quantity for a
    specific product in cart, rather than adding to it.
    """

    try:
        request_payload = json.loads(event["body"])
    except KeyError:
        return {
            "statusCode": 400,
            "headers": get_headers(),
            "body": json.dumps({"message": "No Request payload"}),
        }

    # retrieve the product_id that was specified in the url
    product_id = event["pathParameters"]["product_id"]

    quantity = int(request_payload["quantity"])
    cart_id, _ = get_cart_id(event["headers"])

    # Because this method can be called anonymously, we need to check if there's a logged in user
    user_sub = None
    jwt_token = event["headers"].get("Authorization")
    if jwt_token:
        user_sub = get_user_sub(jwt_token)

    try:
        product = get_product_from_external_service(product_id)
    except NotFoundException:
        logger.info("No product found with product_id: %s", product_id)
        return {
            "statusCode": 404,
            "headers": get_headers(cart_id=cart_id),
            "body": json.dumps({"message": "product not found"}),
        }

    # Prevent storing negative quantities of things
    if quantity < 0:
        return {
            "statusCode": 400,
            "headers": get_headers(cart_id),
            "body": json.dumps(
                {
                    "productId": product_id,
                    "message": "Quantity must not be lower than 0",
                }
            ),
        }

    # Use logged in user's identifier if it exists, otherwise use the anonymous identifier

    if user_sub:
        pk = f"user#{user_sub}"
        ttl = generate_ttl(
            7
        )  # Set a longer ttl for logged in users - we want to keep their cart for longer.
    else:
        pk = f"cart#{cart_id}"
        ttl = generate_ttl()

    table.put_item(
        Item={
            "pk": pk,
            "sk": f"product#{product_id}",
            "quantity": quantity,
            "expirationTime": ttl,
            "productDetail": product,
        }
    )
    logger.info("about to add metrics...")
    metrics.add_metric(name="CartUpdated", unit="Count", value=1)

    return {
        "statusCode": 200,
        "headers": get_headers(cart_id),
        "body": json.dumps(
            {"productId": product_id, "quantity": quantity, "message": "cart updated"}
        ),
    }
