import os

import requests

from shared import NotFoundException

product_service_url = os.environ["PRODUCT_SERVICE_URL"]


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
