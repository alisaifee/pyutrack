from pyutrack import Connection
from pyutrack import Credentials
from pyutrack.errors import LoginError
from tests.integration import IntegrationTest


class AuthenticationTests(IntegrationTest):
    def test_successful_authentication(self):
        connection = Connection(
            credentials=Credentials(username='root', password='root'),
            base_url='http://localhost:9876'
        )
        self.assertTrue(connection.login())

    def test_invalid_password(self):
        connection = Connection(
            credentials=Credentials(username='root', password='rooted'),
            base_url='http://localhost:9876'
        )
        self.assertRaises(LoginError, connection.login)
