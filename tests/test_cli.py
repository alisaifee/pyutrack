#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `pyutrack` package."""

import unittest
from click.testing import CliRunner

from pyutrack import cli
from tests import PyutrackTest


class TestYoutrack_cli(PyutrackTest):
    def test_improt(self):
        import pyutrack

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        assert result.exit_code == 0
        assert 'YouTrack' in result.output
        help_result = runner.invoke(cli.cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output
