import json

def lambda_handler(event, context):
    print("event", event)
    print("context", context)

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
        "principalId": "anonymous",  # or a specific principal based on your use case
        "policyDocument": policy_document
    }
