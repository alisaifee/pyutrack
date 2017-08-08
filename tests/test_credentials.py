from pyutrack import Credentials
from tests import PyutrackTest


class CredentialsTests(PyutrackTest):
    def test_empty(self):
        c = Credentials('root')
        self.assertIsNone(c.password)
        self.assertIsNone(c.cookies)
