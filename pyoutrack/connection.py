import json
import logging

import keyring
import requests

from pyoutrack.errors import ApiError, response_to_exc

logging.basicConfig(level=logging.DEBUG)


class Credentials(object):
    KEYRING_COOKIE = 'youtrack-cli:cookies'
    KEYRING_PASSWORD = 'youtrack-cli:cookies'

    def __init__(self, username, password=None, cookies=None):
        self._username = username
        self._password = password
        self._cookies = cookies
        if not (cookies and password):
            self.load_from_keyring()

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
        cookies = keyring.get_password(Credentials.KEYRING_PASSWORD, self.username)
        if cookies:
            self.cookies = cookies
            return True
        else:
            password = keyring.get_password(Credentials.KEYRING_PASSWORD, self.username)
            if password:
                self.password = password
                return True
        return False
    def persist(self):
        if self.cookies:
            keyring.set_password("youtrack-cli:cookies", self.username, self.cookies)
        if self.password:
            keyring.set_password("youtrack-cli:password", self.username, self.password)

    def reset_cookies(self):
        if keyring.get_password("youtrack-cli:cookies", self.username):
            keyring.delete_password("youtrack-cli:cookies", self.username)
        self.cookies = None

    def reset_password(self):
        if keyring.get_password("youtrack-cli:password", self.username):
            keyring.delete_password("youtrack-cli:password", self.username)
        self.password = None


class Connection(object):
    def __init__(self):
        self.__session = requests.Session()
        self.__session.debug = True
        self.__session.headers.update({"Accept": "application/json"})
        self.__credentials = None
        self.__api_url = ''

    def login(self):
        if self.credentials.cookies:
            self.__session.cookies.update(json.loads(self.credentials.cookies))
            if self.get("user/current").get("email"):
                return True
            else:
                self.credentials.reset_cookies()
        try:
            self.post("user/login", {"login": self.credentials.username, "password": self.credentials.password})
            self.credentials.cookies = json.dumps(self.__session.cookies.get_dict())
            self.credentials.persist()
            return True
        except (ApiError,) as e:
            print(e)
            self.credentials.reset_password()
            return False

    @property
    def credentials(self):
        return self.__credentials

    @credentials.setter
    def credentials(self, credentials):
        self.__credentials = credentials

    @property
    def api_url(self):
        return self.__base_url

    @api_url.setter
    def api_url(self, api_url):
        ref = api_url.rstrip("/")
        if ref.endswith("/rest"):
            self.__api_url = ref
        else:
            self.__api_url = "%s/youtrack/rest" % ref

    def __parse(self, response):
        if not response.ok:
            raise response_to_exc(response)
        if response.status_code == 201 and response.headers.get('location'):
            return self.__session.get(response.headers['location']).json()
        try:
            return response.json()
        except (ValueError,):
            return response.content

    def get(self, path):
        return self.__parse(self.__session.get("%s/%s" % (self.__api_url, path)))

    def post(self, path, data):
        print(path, data)
        return self.__parse(self.__session.post("%s/%s" % (self.__api_url, path), data))

    def put(self, path, data):
        print(path, data)
        return self.__parse(self.__session.put("%s/%s" % (self.__api_url, path), data))

    def delete(self, path):
        return self.__parse(self.__session.delete("%s/%s" % (self.__api_url, path)))


