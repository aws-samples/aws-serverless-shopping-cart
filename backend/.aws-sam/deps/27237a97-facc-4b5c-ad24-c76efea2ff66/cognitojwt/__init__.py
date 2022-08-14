from .exceptions import CognitoJWTException

name = 'cognitojwt'


__all__ = ['CognitoJWTException']


try:
    import requests
    from .jwt_sync import decode
    __all__.append('decode')
except ImportError:
    pass

try:
    import aiohttp
    from async_lru import alru_cache
    from .jwt_async import decode_async
    __all__.append('decode_async')
except ImportError:
    pass
