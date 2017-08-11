import os
import re
import time
import unittest

import requests
import subprocess

import shutil

from requests import RequestException

from pyutrack import Credentials


class PyutrackTest(unittest.TestCase):
    unit = True
    def setUp(self):
        credentials = Credentials(username='root')
        credentials.reset_cookies()
        credentials.reset_password()


class YouTrackServer(object):
    SERVER_DIR = os.path.join(os.path.split(__file__)[0], "tmp")
    COMMAND = '-Xmx1g -XX:MaxMetaspaceSize=250m -Djetbrains.youtrack.disableBrowser=true -Djava.awt.headless=true -Ddatabase.location=%(db_location)s -jar %(jar)s localhost:%(port)d'

    def __init__(
            self,
            version=os.environ.get('YOUTRACK_TEST_SERVER_VERSION', 'latest'),
            port=9876,
            verbose=int(os.environ.get('YOUTRACK_TEST_SERVER_DEBUG', 0))
    ):
        self.__port = port
        self.__proc = None
        self.__timeout = int(os.environ.get('YOUTRACK_TEST_SERVER_TIMEOUT', 120))
        self.__pipe = subprocess.PIPE if not verbose else None
        if version == 'latest':
            self.fetch_latest_version()
        else:
            self.version = version

    def fetch_latest_version(self):
        releases = requests.get(
            "https://data.services.jetbrains.com//products/releases?code=YTD&latest=true&type=release"
        ).json()
        latest = (releases.get('YTD', [])[-1] or {}).get('downloads', {}).get(
            'javaEE', {})
        jar_link = latest.get('link')
        self.version = re.findall('youtrack\-(.*?).jar', jar_link)[
            0] if jar_link else None

    @property
    def download_url(self):
        return 'http://download.jetbrains.com/charisma/%s' % self.jar_name

    @property
    def temp_dir(self):
        return os.path.join(YouTrackServer.SERVER_DIR, self.version)

    @property
    def backup_db_dir(self):
        return os.path.join(
            os.path.split(__file__)[0],
            'configs', 'backup_database/'
        )

    @property
    def db_dir(self):
        return os.path.join(self.temp_dir, 'db/')

    @property
    def jar_name(self):
        return 'youtrack-%s.jar' % self.version

    @property
    def port(self):
        return self.__port

    @property
    def running(self):
        return self.__proc is not None

    def get_jar(self):
        if self.version:
            if not os.path.exists(self.temp_dir):
                os.makedirs(self.temp_dir)
            if not os.path.isfile(os.path.join(self.temp_dir, self.jar_name)):
                jar = requests.get(self.download_url)
                if not jar.ok:
                    return False
                open(os.path.join(
                    self.temp_dir, self.jar_name), 'wb'
                ).write(jar.content)
            return True
        return False

    def start(self):
        if self.get_jar():
            if os.path.isdir(self.db_dir):
                shutil.rmtree(self.db_dir)
            shutil.copytree(self.backup_db_dir, self.db_dir)
            cmd = self.COMMAND % {
                'jar': self.jar_name,
                'db_location': os.path.join(self.temp_dir, 'db'),
                'port': self.port
            }
            self.__proc = subprocess.Popen(
                cmd.split(' '),
                executable='java',
                cwd=self.temp_dir,
                stdout=self.__pipe,
                stderr=self.__pipe
            )
            if not self.wait_for_startup():
                self.__proc.kill()
                raise Exception(
                    "Unable to start youtrack %s on port %d within %d seconds" %
                    (self.version, self.port, self.__timeout)
                )

    def save_database(self):
        if os.path.isdir(self.backup_db_dir):
            shutil.rmtree(self.backup_db_dir)
        shutil.copytree(self.db_dir, self.backup_db_dir)

    def wait_for_startup(self):
        url = 'http://localhost:%d/rest/user/current' % self.port
        start = time.time()

        def _():
            try:
                return requests.get(url, timeout=1).ok
            except RequestException:
                return False

        while not _():
            time.sleep(1)
            if time.time() - start > self.__timeout:
                return False
        return True

    def stop(self):
        if self.__proc:
            self.__proc.terminate()
