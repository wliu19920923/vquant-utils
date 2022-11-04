from bson import ObjectId
from jwt import ExpiredSignatureError, InvalidTokenError
from tornado.web import HTTPError
from exceptions import PermissionDenied, InvalidToken


def allow(method):
    async def wrapper(self, *args, **kwargs):
        code, data, message = 200, None, None
        try:
            data = await method(self, *args, **kwargs)
        except HTTPError as exp:
            code, message = exp.status_code, exp.log_message
        self.set_status(code)
        self.write(dict(data=data, message=message))
        await self.finish()

    return wrapper


def authenticated(method):
    async def wrapper(self, *args, **kwargs):
        code, data, message = 200, None, None
        try:
            token = self.get_cookie(type(self.settings['jwt']).__name__, None)
            payload = self.settings['jwt'].decode(token)
            self.current_user = payload
            self.current_user['_id'] = ObjectId(self.current_user['_id'])
            data = await method(self, *args, **kwargs)
        except (InvalidTokenError, ExpiredSignatureError, InvalidTokenError):
            code, message = InvalidToken.status_code, InvalidToken.log_message
        except HTTPError as exp:
            code, message = exp.status_code, exp.log_message
        self.set_status(code)
        self.write(dict(data=data, message=message))
        await self.finish()

    return wrapper


def superuser(method):
    async def wrapper(self, *args, **kwargs):
        code, data, message = 200, None, None
        try:
            token = self.get_cookie(type(self.settings['jwt']).__name__, None)
            payload = self.settings['jwt'].decode(token)
            self.current_user = payload
            if not self.current_user['is_superuser']:
                raise PermissionDenied
            self.current_user['_id'] = ObjectId(self.current_user['_id'])
            data = await method(self, *args, **kwargs)
        except (InvalidTokenError, ExpiredSignatureError, InvalidTokenError):
            code, message = InvalidToken.status_code, InvalidToken.log_message
        except HTTPError as exp:
            code, message = exp.status_code, exp.log_message
        self.set_status(code)
        self.write(dict(data=data, message=message))
        await self.finish()

    return wrapper


def staff(method):
    async def wrapper(self, *args, **kwargs):
        code, data, message = 200, None, None
        try:
            token = self.get_cookie(type(self.settings['jwt']).__name__, None)
            payload = self.settings['jwt'].decode(token)
            self.current_user = payload
            if not self.current_user['is_staff']:
                raise PermissionDenied
            self.current_user['_id'] = ObjectId(self.current_user['_id'])
            data = await method(self, *args, **kwargs)
        except (InvalidTokenError, ExpiredSignatureError, InvalidTokenError):
            code, message = InvalidToken.status_code, InvalidToken.log_message
        except HTTPError as exp:
            code, message = exp.status_code, exp.log_message
        self.set_status(code)
        self.write(dict(data=data, message=message))
        await self.finish()

    return wrapper
