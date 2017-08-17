import six


class ErrorRegistry(type):
    REGISTRY = {}

    def __new__(mcs, name, bases, dct):
        cls = super(ErrorRegistry, mcs).__new__(mcs, name, bases, dct)
        [
            ErrorRegistry.REGISTRY.setdefault(code, cls)
            for code in dct.get('CODES', [])
        ]
        return cls


@six.add_metaclass(ErrorRegistry)
class ApiError(Exception):
    def __init__(self, response):
        self.status = response.status_code
        try:
            message = response.json()['value']
        except (ValueError, KeyError):
            message = response.content
        super(ApiError, self).__init__("%s" % message)


class PermissionsError(ApiError):
    CODES = [403, 407, 429]


class AuthorizationError(ApiError):
    CODES = [401]


class InputError(ApiError):
    CODES = [400, 405, 405, 409, 412, 413]


class NotFoundError(ApiError):
    CODES = [404]


class LoginError(Exception):
    pass


class ResponseError(Exception):
    pass


class CliError(Exception):
    pass


def response_to_exc(response):
    return ErrorRegistry.REGISTRY.get(response.status_code, ApiError)(response)
