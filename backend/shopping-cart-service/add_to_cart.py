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
import datetime
import time

logger = Logger()
tracer = Tracer()
metrics = Metrics()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
product_service_url = os.environ["PRODUCT_SERVICE_URL"]
pinpoint = boto3.client('pinpoint')
pinpoint_app_id = 'd8bc2f39610240d2a87774aa074e5fb6'
pinpoint_address = 'udom@brikl.com'

@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    Add a the provided quantity of a product to a cart. Where an item already exists in the cart, the quantities will
    be summed.
    """

    try:
        request_payload = json.loads(event["body"])
    except KeyError:
        return {
            "statusCode": 400,
            "headers": get_headers(),
            "body": json.dumps({"message": "No Request payload"}),
        }
    product_id = request_payload["productId"]
    quantity = request_payload.get("quantity", 1)
    cart_id, _ = get_cart_id(event["headers"])

    # Because this method can be called anonymously, we need to check there's a logged in user
    user_sub = None
    jwt_token = event["headers"].get("Authorization")
    if jwt_token:
        user_sub = get_user_sub(jwt_token)

    try:
        product = get_product_from_external_service(product_id)
        logger.info("No product found with product_id: %s", product_id)
    except NotFoundException:
        return {
            "statusCode": 404,
            "headers": get_headers(cart_id=cart_id),
            "body": json.dumps({"message": "product not found"}),
        }

    if user_sub:
        logger.info("Authenticated user")
        pk = f"user#{user_sub}"
        ttl = generate_ttl(
            7
        )  # Set a longer ttl for logged in users - we want to keep their cart for longer.
    else:
        logger.info("Unauthenticated user")
        pk = f"cart#{cart_id}"
        ttl = generate_ttl()

    if int(quantity) < 0:
        table.update_item(
            Key={"pk": pk, "sk": f"product#{product_id}"},
            ExpressionAttributeNames={
                "#quantity": "quantity",
                "#expirationTime": "expirationTime",
                "#productDetail": "productDetail",
            },
            ExpressionAttributeValues={
                ":val": quantity,
                ":ttl": ttl,
                ":productDetail": product,
                ":limit": abs(quantity),
            },
            UpdateExpression="ADD #quantity :val SET #expirationTime = :ttl, #productDetail = :productDetail",
            # Prevent quantity less than 0
            ConditionExpression="quantity >= :limit",
        )
    else:
        table.update_item(
            Key={"pk": pk, "sk": f"product#{product_id}"},
            ExpressionAttributeNames={
                "#quantity": "quantity",
                "#expirationTime": "expirationTime",
                "#productDetail": "productDetail",
            },
            ExpressionAttributeValues={
                ":val": quantity,
                ":ttl": generate_ttl(),
                ":productDetail": product,
            },
            UpdateExpression="ADD #quantity :val SET #expirationTime = :ttl, #productDetail = :productDetail",
        )
    metrics.add_metric(name="CartUpdated", unit="Count", value=1)

    pinpoint.put_events(
        ApplicationId = pinpoint_app_id,
        EventsRequest={
            'BatchItem': {
                user_sub: {
                    'Endpoint': {
                        'ChannelType': 'EMAIL',
                        'Address': pinpoint_address,
                        'Attributes': {
                            'Cart': ['Hat'],
                            'Purchased': ['No']
                        }
                    },
                    'Events':{
                        'cart-event-2': {
                            'Attributes':{
                                'AddedToCart': 'Hat'
                            },
                            'EventType': 'AddToCartEvent',
                            'Metrics': {
                                'price': 29.95
                            },
                            'Timestamp': datetime.datetime.fromtimestamp(time.time()).isoformat()
                        }
                    }
                }
            } 
        }
    )

    return {
        "statusCode": 200,
        "headers": get_headers(cart_id),
        "body": json.dumps(
            {"productId": product_id, "message": "product added to cart"}
        ),
    }
