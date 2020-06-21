import calendar
import datetime
import os
import uuid
from decimal import Decimal
from http.cookies import SimpleCookie

from aws_lambda_powertools import Tracer

import cognitojwt

tracer = Tracer()

HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN"),
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    "Access-Control-Allow-Credentials": True,
}


class NotFoundException(Exception):
    pass


@tracer.capture_method
def handle_decimal_type(obj):
    """
    json serializer which works with Decimal types returned from DynamoDB.
    """
    if isinstance(obj, Decimal):
        if float(obj).is_integer():
            return int(obj)
        else:
            return float(obj)
    raise TypeError


@tracer.capture_method
def generate_ttl(days=1):
    """
    Generate epoch timestamp for number days in future
    """
    future = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    return calendar.timegm(future.utctimetuple())


@tracer.capture_method
def get_user_sub(jwt_token):
    """
    Validate JWT claims & retrieve user identifier
    """
    try:
        verified_claims = cognitojwt.decode(
            jwt_token, os.environ["AWS_REGION"], os.environ["USERPOOL_ID"]
        )
    except (cognitojwt.CognitoJWTException, ValueError):
        verified_claims = {}

    return verified_claims.get("sub")


@tracer.capture_method
def get_cart_id(event_headers):
    """
    Retrieve cart_id from cookies if it exists, otherwise set and return it
    """
    cookie = SimpleCookie()
    try:
        cookie.load(event_headers["cookie"])
        cart_cookie = cookie["cartId"].value
        generated = False
    except KeyError:
        cart_cookie = str(uuid.uuid4())
        generated = True

    return cart_cookie, generated


@tracer.capture_method
def get_headers(cart_id):
    """
    Get the headers to add to response data
    """
    headers = HEADERS
    cookie = SimpleCookie()
    cookie["cartId"] = cart_id
    cookie["cartId"]["max-age"] = (60 * 60) * 24  # 1 day
    cookie["cartId"]["secure"] = True
    cookie["cartId"]["httponly"] = True
    cookie["cartId"]["samesite"] = "None"
    cookie["cartId"]["path"] = "/"
    headers["Set-Cookie"] = cookie["cartId"].OutputString()
    return headers
