#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyoutrack` package."""


import unittest
from click.testing import CliRunner

from pyoutrack import cli


class TestYoutrack_cli(unittest.TestCase):

    def test_improt(self):
        import pyoutrack

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        assert result.exit_code == 0
        assert 'YouTrack CLI' in result.output
        help_result = runner.invoke(cli.cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output
