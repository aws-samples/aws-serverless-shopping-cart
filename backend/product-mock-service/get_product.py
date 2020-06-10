import json
import os

from aws_lambda_powertools import Logger, Tracer

from mock_product_list import PRODUCT_LIST

logger = Logger()
tracer = Tracer()


HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN"),
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    Return single product based on path parameter.
    """

    path_params = event["pathParameters"]
    product_id = path_params.get("product_id")
    logger.debug("Retriving product_id: %s", product_id)
    product = next(
        (item for item in PRODUCT_LIST if item["productId"] == product_id), None
    )

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({"product": product}),
    }
