from typing import List, Dict

import aiohttp
from async_lru import alru_cache
from jose import jwk
from jose.utils import base64url_decode

from .constants import PUBLIC_KEYS_URL_TEMPLATE
from .exceptions import CognitoJWTException
from .token_utils import get_unverified_headers, get_unverified_claims, check_expired, check_client_id


@alru_cache(maxsize=1)
async def get_keys_async(keys_url: str) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(keys_url) as resp:
            response = await resp.json()
            return response.get('keys')


async def get_public_key_async(token: str, region: str, userpool_id: str):
    keys_url: str = PUBLIC_KEYS_URL_TEMPLATE.format(region, userpool_id)
    keys: list = await get_keys_async(keys_url)
    headers = get_unverified_headers(token)
    kid = headers['kid']

    key = list(filter(lambda k: k['kid'] == kid, keys))
    if not key:
        raise CognitoJWTException('Public key not found in jwks.json')
    else:
        key = key[0]

    return jwk.construct(key)


async def decode_async(
        token: str,
        region: str,
        userpool_id: str,
        app_client_id: str = None,
        testmode: bool = False
) -> Dict:
    message, encoded_signature = str(token).rsplit('.', 1)

    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    public_key = await get_public_key_async(token, region, userpool_id)

    if not public_key.verify(message.encode('utf-8'), decoded_signature):
        raise CognitoJWTException('Signature verification failed')

    claims = get_unverified_claims(token)
    check_expired(claims['exp'], testmode=testmode)

    if app_client_id:
        check_client_id(claims, app_client_id)

    return claims


__all__ = [
    'decode_async'
]
