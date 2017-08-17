import os

import anyconfig

from pyutrack import Credentials


class Config(object):
    DEFAULT_PATH = os.path.expanduser('~/.pyutrack')

    def __init__(self, path=DEFAULT_PATH):
        self.__config = {}
        self.__path = path
        self.__load()

    def __load(self):
        if not os.path.isfile(self.__path):
            return
        self.__config = anyconfig.load(
            self.__path,
            ac_parser=not os.path.splitext(self.__path)[1] and 'ini'
        ).get('pyutrack', {})

    def reload(self):
        self.__load()
        return self

    def persist(self):
        anyconfig.dump({'pyutrack': self.__config}, self.__path, 'ini')

    @property
    def persisted(self):
        return os.path.isfile(self.__path)

    @property
    def credentials(self):
        return Credentials(
            self.__config.get('username'), self.__config.get('password')
        )

    @credentials.setter
    def credentials(self, value):
        self.__config['username'] = value.username
        self.__config['password'] = value.password

    @property
    def base_url(self):
        return self.__config.get('base_url')

    @base_url.setter
    def base_url(self, value):
        self.__config['base_url'] = value
