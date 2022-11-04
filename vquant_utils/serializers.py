import re
import json
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from tornado.web import HTTPError, RequestHandler


class BooleanField(object):
    def __init__(self, default: int = None, required: bool = True):
        self.default = default
        self.required = required

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        if value not in ('0', '1'):
            raise HTTPError(400, 'Field %s must be a boolean value, 0 or 1' % field)
        value = int(value)
        return value


class CharField(object):
    def __init__(self, default: str = None, required: bool = True, min_length: int = 0, max_length: int = 0, choices: tuple = tuple()):
        self.default = default
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.choices = choices

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        if self.min_length and len(value) < self.min_length:
            raise HTTPError(400, 'Field %s has at least %d characters' % (field, self.min_length))
        if self.max_length and len(value) > self.max_length:
            raise HTTPError(400, 'Field %s has no more than %d characters' % (field, self.min_length))
        return value or self.default


class EmailField(object):
    def __init__(self, default: float = None, required: bool = True):
        self.default = default
        self.required = required

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        if not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+', value):
            raise HTTPError(400, 'Field %s must be a valid email address' % field)
        return value or self.default


class FloatField(object):
    def __init__(self, default: float = None, required: bool = True, min_value: float = 0, max_value: float = 0, choices: tuple = tuple()):
        self.default = default
        self.required = required
        self.min_value = min_value
        self.max_value = max_value
        self.choices = choices

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        if not value.strip('-').replace('.', '').isdigit():
            raise HTTPError(400, 'Field %s must be a valid float number' % field)
        value = float(value)
        if self.min_value and value < self.min_value:
            raise HTTPError(400, 'Field %s is greater than or equal to %f' % (field, self.min_value))
        if self.max_value and value > self.max_value:
            raise HTTPError(400, 'Field %s is less than or equal to %f' % (field, self.max_value))
        return value or self.default


class IntegerField(object):
    def __init__(self, default: int = None, required: bool = True, min_value: int = 0, max_value: int = 0, choices: tuple = tuple()):
        self.default = default
        self.required = required
        self.min_value = min_value
        self.max_value = max_value
        self.choices = choices

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        if not value.isdigit():
            raise HTTPError(400, 'Field %s must be a valid integer' % field)
        value = int(value)
        if self.min_value and value < self.min_value:
            raise HTTPError(400, 'Field %s is greater than or equal to %d' % (field, self.min_value))
        if self.max_value and value > self.max_value:
            raise HTTPError(400, 'Field %s is less than or equal to %d' % (field, self.max_value))
        return value


class IpAddressField(object):
    def __init__(self, default: float = None, required: bool = True):
        self.default = default
        self.required = required

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        if not re.match('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$', value):
            raise HTTPError(400, 'Field %s must be a valid ip address' % field)
        return value or self.default


class JSONField(object):
    def __init__(self, default: dict = None, required: bool = True):
        self.default = default
        self.required = required

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            raise HTTPError(400, 'Field %s must be a valid json string' % field)
        return value or self.default


class ObjectIdField(object):
    def __init__(self, default: ObjectId = None, required: bool = True, choices: tuple = tuple()):
        self.default = default
        self.required = required
        self.choices = choices

    def validate(self, field, value):
        if not self.required and value is None:
            return value or self.default
        if value is None:
            raise HTTPError(400, 'Field %s required' % field)
        try:
            value = ObjectId(value)
        except InvalidId:
            raise HTTPError(400, 'Field %s must be a 24-character hex string' % field)
        return value


class Serializer(object):
    def __init__(self, request: RequestHandler, **arguments):
        self.request = request
        self.arguments = arguments

    @property
    def validated_data(self):
        result = dict()
        for field, serializer in self.arguments.items():
            value = self.request.get_argument(field, None)
            value = serializer.validate(field, value)
            if value is not None:
                result[field] = value
        return result


class ModelSerializer(object):
    def __init__(self, document, exclude_fields: tuple = tuple()):
        self.document = document
        self.exclude_fields = exclude_fields

    @property
    def data(self):
        result = dict()
        for key in self.document:
            if key not in self.exclude_fields:
                if isinstance(self.document[key], ObjectId):
                    result[key] = str(self.document[key])
                elif isinstance(self.document[key], datetime):
                    result[key] = int(self.document[key].timestamp() * 1000)
                else:
                    result[key] = self.document[key]
        return result
