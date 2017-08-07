import os

import anyconfig

from pyutrack import Credentials

CONFIG_PATH = os.path.expanduser('~/.pyutrack')


class Config(object):
    def __init__(self, path=CONFIG_PATH):
        self.__config = {}
        self.__load(path, allow_not_exist=path == CONFIG_PATH)

    def __load(self, path, allow_not_exist):
        if allow_not_exist and not os.path.isfile(path):
            return
        self.__config = anyconfig.load(path, ac_parser=not os.path.splitext(path)[1] and 'yaml')

    @property
    def credentials(self):
        if 'username' in self.__config:
            return Credentials(self.__config.get('username'), self.__config.get('password'))

    @property
    def base_url(self):
        return self.__config.get('base_url')
