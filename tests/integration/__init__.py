import unittest

import atexit

from tests import YouTrackServer

SERVER = YouTrackServer()


class IntegrationTest(unittest.TestCase):
    integration = True
    @classmethod
    def setUpClass(cls):
        if not SERVER.running:
            SERVER.start()


atexit.register(lambda: SERVER.running and SERVER.stop())
