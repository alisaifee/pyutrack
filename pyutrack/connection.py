import json

import keyring
import requests

from pyutrack.errors import response_to_exc, AuthorizationError, LoginError, PermissionsError, ResponseError


class Credentials(object):
    KEYRING_COOKIE = 'pyutrack:cookies'
    KEYRING_PASSWORD = 'pyutrack:password'

    def __init__(self, username, password=None, cookies=None):
        self._username = username
        self._cookies = None
        self._password = None
        self.load_from_keyring()
        if password:
            self._password = password
        if cookies:
            self._cookies = cookies

    @staticmethod
    def from_keyring(username):
        ytc = Credentials(username)
        if ytc.load_from_keyring():
            return ytc

    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, value):
        self._cookies = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def load_from_keyring(self):
        keyring_cookie = keyring.get_password(
            Credentials.KEYRING_COOKIE, self.username
        )
        cookies = json.loads(keyring_cookie) if keyring_cookie else None
        password = keyring.get_password(
            Credentials.KEYRING_PASSWORD, self.username
        )
        if cookies:
            self.cookies = cookies
        if password:
            self.password = password
        return cookies or password

    def persist(self):
        if self.cookies:
            keyring.set_password(
                self.KEYRING_COOKIE, self.username, json.dumps(self.cookies)
            )
        if self.password:
            keyring.set_password(
                self.KEYRING_PASSWORD, self.username, self.password
            )

    def reset_cookies(self):
        if keyring.get_password(self.KEYRING_COOKIE, self.username):
            keyring.delete_password(self.KEYRING_COOKIE, self.username)
        self.cookies = None

    def reset_password(self):
        if keyring.get_password(self.KEYRING_PASSWORD, self.username):
            keyring.delete_password(self.KEYRING_PASSWORD, self.username)
        self.password = None


def fix_auth(meth):
    def inner(self, *args, **kwargs):
        try:
            return meth(self, *args, **kwargs)
        except (AuthorizationError, ) as e:
            if self.credentials.cookies:
                self.credentials.reset_cookies()
                if self.credentials.password:
                    self.login()
                    return meth(self, *args, **kwargs)
            raise e

    return inner


class Connection(object):
    def __init__(self, base_url=None, credentials=None):
        self.__session = requests.Session()
        self.__session.debug = True
        self.__session.headers.update({'Accept': 'application/json'})
        self.__session_args = {}
        self.__credentials = credentials
        if self.credentials and self.credentials.cookies:
            self.__session.cookies.update(credentials.cookies)
        self.__api_url = ''
        if base_url:
            self.api_url = base_url

    def login(self, persist_credentials=True):
        try:
            self.post(
                'user/login', {
                    'login': self.credentials.username,
                    'password': self.credentials.password
                }, False
            )
            self.credentials.cookies = self.__session.cookies.get_dict()
            if persist_credentials:
                self.credentials.persist()
            return True
        except (PermissionsError, ) as e:
            raise LoginError(e)

    @property
    def credentials(self):
        return self.__credentials

    @credentials.setter
    def credentials(self, credentials):
        if credentials.cookies:
            self.__session.cookies.update(credentials.cookies)
        self.__credentials = credentials

    @property
    def api_url(self):
        return self.__api_url

    @api_url.setter
    def api_url(self, api_url):
        ref = api_url.rstrip('/')
        if ref.endswith('/rest'):
            self.__api_url = ref
        else:
            self.__api_url = '%s/rest' % ref

    @fix_auth
    def get(self, path, parse=True):
        return self.__unwrap(
            self.__session.get(
                '%s/%s' % (self.__api_url, path), **self.__session_args
            ), parse
        )

    @fix_auth
    def post(self, path, data, parse=True):
        return self.__unwrap(
            self.__session.post(
                '%s/%s' % (self.__api_url, path), data, **self.__session_args
            ), parse
        )

    @fix_auth
    def put(self, path, data, parse=True):
        return self.__unwrap(
            self.__session.put(
                '%s/%s' % (self.__api_url, path), data, **self.__session_args
            ), parse
        )

    @fix_auth
    def delete(self, path, parse=False):
        return self.__unwrap(
            self.__session.delete(
                '%s/%s' % (self.__api_url, path), **self.__session_args
            ), parse
        )

    def __unwrap(self, response, parse):
        if not response.ok:
            raise response_to_exc(response)
        if response.status_code == 201 and response.headers.get('location'):
            return self.__session.get(response.headers['location']).json()
        if not parse:
            return response.content
        try:
            return response.json()
        except (ValueError, ):
            raise ResponseError('Unexpected response format from server')
