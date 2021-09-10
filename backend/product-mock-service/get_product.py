import json
import os


with open("product_list.json", "r") as product_list:
    product_list = json.load(product_list)

HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN"),
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}


def lambda_handler(event, context):
    """
    Return single product based on path parameter.
    """
    path_params = event["pathParameters"]
    product_id = path_params.get("product_id")
    product = next(
        (item for item in product_list if item["productId"] == product_id), None
    )

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({"product": product}),
    }
