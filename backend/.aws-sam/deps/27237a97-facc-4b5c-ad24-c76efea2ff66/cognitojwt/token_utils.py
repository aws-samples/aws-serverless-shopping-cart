import time

from typing import Dict
from jose import jwt

from .exceptions import CognitoJWTException


CLIENT_ID_KEYS: Dict[str, str] = {
    'access': 'client_id',
    'id': 'aud'
}


def get_unverified_headers(token: str) -> dict:
    return jwt.get_unverified_headers(token)


def get_unverified_claims(token: str) -> dict:
    return jwt.get_unverified_claims(token)


def check_expired(exp: int, testmode: bool = False) -> None:
    if time.time() > exp and not testmode:
        raise CognitoJWTException('Token is expired')


def check_client_id(claims: Dict, app_client_id: str) -> None:
    token_use = claims['token_use']

    client_id_key: str = CLIENT_ID_KEYS.get(token_use)
    if not client_id_key:
        raise CognitoJWTException(f'Invalid token_use: {token_use}. Valid values: {list(CLIENT_ID_KEYS.keys())}')

    if claims[client_id_key] != app_client_id:
        raise CognitoJWTException('Token was not issued for this client id audience')


__all__ = [
    'get_unverified_headers',
    'get_unverified_claims',
    'check_expired',
    'check_client_id'
]
