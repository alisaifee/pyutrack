import json

import keyring

from pyutrack import Credentials
from tests import PyutrackTest


class CredentialsTests(PyutrackTest):
    def test_empty(self):
        c = Credentials('root')
        self.assertIsNone(c.password)
        self.assertIsNone(c.cookies)

    def test_persistence(self):
        c = Credentials('root', 'passwd', {"key": "value"})
        c.persist()
        self.assertEqual(
            keyring.get_password(Credentials.KEYRING_PASSWORD, 'root'), 'passwd'
        )
        self.assertEqual(
            json.loads(keyring.get_password(Credentials.KEYRING_COOKIE, 'root')),
            {"key": "value"}

        )

    def test_reload(self):
        Credentials('root', 'passwd', {"key": "value"}).persist()
        c = Credentials('root')
        self.assertEqual(
            keyring.get_password(Credentials.KEYRING_PASSWORD, 'root'), 'passwd'
        )
        self.assertEqual(
            json.loads(keyring.get_password(Credentials.KEYRING_COOKIE, 'root')),
            {"key": "value"}

        )

