import json
import os
import boto3
from aws_lambda_powertools import Logger, Tracer
from shared import get_user_claims

logger = Logger()
tracer = Tracer()

# Load different product lists
with open('product_list.json', 'r') as regular_product_list_file:
    regular_product_list = json.load(regular_product_list_file)
with open('admin_product_list.json', 'r') as admin_product_list_file:
    admin_product_list = json.load(admin_product_list_file)
with open('publisher_product_list.json', 'r') as publisher_product_list_file:
    publisher_product_list = json.load(publisher_product_list_file)

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

    print("User info:", user_info)

    # Construct the authz_request
    authz_request = construct_authz_request(user_info)
    print("authz_request:", authz_request)

    # Make the isAuthorized call
    response = verified_permissions_client.is_authorized(**authz_request)
    print("Authorization response:", response)

    # Determine which product list to return
    product_list = determine_product_list(response, user_info)

    logger.debug("Returning product list")
    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({"products": product_list}),
    }

def construct_authz_request(user_info):
    entities = [
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

    resource = {
        "entityType": "Bookstore::Book",
        "entityId": "*"
    }

    if user_info["role"] == "publisher":
        # For publisher, set the resource to their specific book
        resource["entityId"] = "DantesAdventures"
        entities.append(get_publisher_book_entity(user_info["username"]))

    return {
        "policyStoreId": os.environ.get("POLICY_STORE_ID"),
        "principal": {
            "entityType": "Bookstore::User",
            "entityId": user_info["username"]
        },
        "action": {
            "actionType": "Bookstore::Action",
            "actionId": "View"
        },
        "resource": resource,
        "entities": {"entityList": entities},
        "context": {"contextMap": {}}
    }

def get_publisher_book_entity(username):
    # This method returns the entity for the publisher's book
    return {
        "identifier": {
            "entityType": "Bookstore::Book",
            "entityId": "DantesAdventures"
        },
        "attributes": {
            "owner": {
                "entityIdentifier": {
                    "entityType": "Bookstore::User",
                    "entityId": username
                }
            }
        },
        "parents": []
    }

def determine_product_list(response, user_info):
    if 'decision' in response and response['decision'] == 'ALLOW':
        policy_description = get_policy_description(response)
        if policy_description == "Allows the publisher to see the books he has published":
            return publisher_product_list
        elif user_info["role"] == "admin":
            return admin_product_list
    return regular_product_list

def get_policy_description(response):
    # Extract the policy ID from the response
    policy_id = response.get('determiningPolicies', [{}])[0].get('policyId')
    if policy_id:
        policy_response = verified_permissions_client.get_policy(
            policyStoreId=os.environ.get("POLICY_STORE_ID"),
            policyId=policy_id
        )
        return policy_response.get('definition', {}).get('static', {}).get('description')
    return ""
