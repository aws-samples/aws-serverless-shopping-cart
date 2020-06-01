import os

import requests
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer

from shared import NotFoundException

product_service_url = os.environ["PRODUCT_SERVICE_URL"]

logger = Logger(service="shopping-cart")
tracer = Tracer(service="shopping-cart")


@tracer.capture_method
def get_product_from_external_service(product_id):
    """
    Call product API to retrieve product details
    """
    response = requests.get(product_service_url + f"/product/{product_id}")
    try:
        response_dict = response.json()["product"]
    except KeyError:
        raise NotFoundException

    return response_dict
