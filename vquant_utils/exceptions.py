from tornado.web import HTTPError

InvalidToken = HTTPError(401, 'InvalidToken')
PermissionDenied = HTTPError(403, 'PermissionDenied')
TooOften = HTTPError(429, 'TooOften')
