import os
from collections import Counter

import boto3
from boto3.dynamodb import types

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

deserializer = types.TypeDeserializer()


def dynamodb_to_python(dynamodb_item):
    """
    Convert from dynamodb low level format to python dict
    """
    return {k: deserializer.deserialize(v) for k, v in dynamodb_item.items()}


def lambda_handler(event, context):
    """
    Handle streams from DynamoDB table
    """

    records = event["Records"]
    quantity_change_counter = Counter()

    for record in records:
        keys = dynamodb_to_python(record["dynamodb"]["Keys"])
        # NewImage record only exists if the event is INSERT or MODIFY
        if record["eventName"] in ("INSERT", "MODIFY"):
            new_image = dynamodb_to_python(record["dynamodb"]["NewImage"])
        else:
            new_image = {}

        old_image_ddb = record["dynamodb"].get("OldImage")

        if old_image_ddb:
            old_image = dynamodb_to_python(
                record["dynamodb"].get("OldImage")
            )  # Won't exist in case event is INSERT
        else:
            old_image = {}

        # We want to record the quantity change the change made to the db rather than absolute values
        if keys["sk"].startswith("product#"):
            quantity_change_counter.update(
                {
                    keys["sk"]: new_image.get("quantity", 0)
                    - old_image.get("quantity", 0)
                }
            )

    for k, v in quantity_change_counter.items():
        table.update_item(
            Key={"pk": k, "sk": "totalquantity"},
            ExpressionAttributeNames={"#quantity": "quantity"},
            ExpressionAttributeValues={":val": v},
            UpdateExpression="ADD #quantity :val",
        )

    return {
        "statusCode": 200,
    }
