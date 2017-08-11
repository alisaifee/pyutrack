import unittest

import atexit

from tests import YouTrackServer, PyutrackTest

SERVER = YouTrackServer()


class IntegrationTest(PyutrackTest):
    unit = False

    @classmethod
    def setUpClass(cls):
        if not SERVER.running:
            SERVER.start()


atexit.register(lambda: SERVER.running and SERVER.stop())
