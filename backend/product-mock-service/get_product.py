import json
import logging
import os

from mock_product_list import PRODUCT_LIST

logger = logging.getLogger()
logger.setLevel(os.environ['LOG_LEVEL'])

HEADERS = {'Access-Control-Allow-Origin': 'http://localhost:8080',
           "Access-Control-Allow-Headers": "Content-Type",
           "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
           }


def lambda_handler(event, context):
    """
    Return single product based on path parameter.
    """
    logger.debug(event)

    path_params = event['pathParameters']
    product_id = path_params.get('product_id')

    product = next((item for item in PRODUCT_LIST if item["productId"] == product_id), None)

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps(
            {'product': product}
        )
    }
