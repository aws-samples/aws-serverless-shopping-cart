import json

from shared import (
    get_user_claims,
)

def lambda_handler(event, context):
    print("event", event)
    print("context", context)

    jwt_token = event["headers"].get("authorization")

    user_info = {"username": "Unknown", "role": "Unknown"}
    if jwt_token:
        print("if jwt_token:", jwt_token)  # Print the user info

        user_info = get_user_claims(jwt_token)

    print("User info:", user_info)  # Print the user info

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "execute-api:Invoke",
                "Effect": "Allow",
                "Resource": event["methodArn"]
            }
        ]
    }

    return {
        "principalId": user_info.get("username", "Unknown"),
        "policyDocument": policy_document
    }
