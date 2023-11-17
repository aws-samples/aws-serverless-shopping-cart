import json
import os
import boto3

from aws_lambda_powertools import Logger, Tracer

from shared import (
    get_user_claims,
)

logger = Logger()
tracer = Tracer()

with open('product_list.json', 'r') as product_list_file:
    regular_product_list = json.load(product_list_file)

with open('admin_product_list.json', 'r') as admin_product_list_file:
    admin_product_list = json.load(admin_product_list_file)

HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN"),
    "Access-Control-Allow-Headers": "Content-Type,Authorization,authorization",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    "Access-Control-Allow-Credentials": True,
}

verified_permissions_client = boto3.client('verifiedpermissions')


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    print("event", event)
    print("context", context)

    jwt_token = event["headers"].get("Authorization")

    user_info = {"username": "Unknown", "role": "Unknown"}
    if jwt_token:

        user_info = get_user_claims(jwt_token)

    authz_request = {
    "policyStoreId": os.environ.get("POLICY_STORE_ID"),
    "principal": {
        "entityType": "Bookstore::User",
        "entityId": user_info["username"]
    },
    "action": {
        "actionType": "Bookstore::Action",
        "actionId": "View"
    },
    "resource": {
        "entityType": "Bookstore::Book",
        "entityId": "*"
    },
    "entities": {
        "entityList": [
            {
                "identifier": {
                    "entityType": "Bookstore::User",
                    "entityId": user_info["username"]
                },
                "attributes": {},
                "parents": [
                    {
                        "entityType": "Bookstore::Role",
                        "entityId": user_info["role"]
                    }
                ]
            }
        ]
    },
    "context": {
        "contextMap": {}
    }
}
    print("authz_request:", authz_request)

    response = verified_permissions_client.is_authorized(**authz_request)
    print("Authorization response:", response)

    # Initialize product list as regular by default
    product_list = regular_product_list

    # Check if determiningPolicies is not empty and contains at least one policyId
    if response.get('determiningPolicies') and response['determiningPolicies'][0].get('policyId'):
        # Fetch the first policy ID from the determiningPolicies list
        policy_id = response['determiningPolicies'][0]['policyId']
        policy_response = verified_permissions_client.get_policy(
            policyStoreId=os.environ.get("POLICY_STORE_ID"),
            policyId=policy_id
        )
        policy_description = policy_response.get('definition', {}).get('static', {}).get('description')
        print("policy_description response:", policy_description)

        # Check if decision is 'ALLOW' and description matches specific criteria
        if response['decision'] == 'ALLOW' and policy_description == "Allows Admin to see all books":
            product_list = admin_product_list

    logger.debug("Fetching product list")
    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({"products": product_list}),
    }