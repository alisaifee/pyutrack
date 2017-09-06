# -*- coding: utf-8 -*-
"""Top-level package for YouTrack CLI."""

__author__ = """Ali-Akber Saifee"""
__email__ = 'ali@indydevs.org'

from pyutrack.connection import Connection, Credentials
from pyutrack.resources import *

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
