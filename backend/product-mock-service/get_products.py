import json
import logging
import os

from mock_product_list import PRODUCT_LIST

logger = logging.getLogger()
logger.setLevel(os.environ['LOG_LEVEL'])

HEADERS = {'Access-Control-Allow-Origin': os.environ.get('ALLOWED_ORIGIN'),
           "Access-Control-Allow-Headers": "Content-Type",
           "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
           }


def lambda_handler(event, context):
    """
    Return list of all products.
    """
    logger.debug(event)

    product_list = PRODUCT_LIST

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps(
            {'products': product_list}
        )
    }
