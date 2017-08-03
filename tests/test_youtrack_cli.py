#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `youtrack_cli` package."""


import unittest
from click.testing import CliRunner

from youtrack_cli import youtrack_cli
from youtrack_cli import cli


class TestYoutrack_cli(unittest.TestCase):

    def test_improt(self):
        import youtrack_cli

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'youtrack_cli.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
