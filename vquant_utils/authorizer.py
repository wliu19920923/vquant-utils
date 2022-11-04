from datetime import datetime, timedelta
from jwt import decode, encode, InvalidTokenError


class JWToken(object):
    def __init__(self, key):
        self.key = key

    def decode(self, token):
        if not token:
            raise InvalidTokenError
        payload = decode(token.encode('utf-8'), self.key, leeway=timedelta(days=1), algorithms=['HS256'], options={'verify_exp': True})
        return payload['sub']

    def encode(self, sub):
        return encode({
            'exp': datetime.now() + timedelta(days=1),
            'iat': datetime.now(),
            'sub': sub
        }, self.key)
