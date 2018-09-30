# -*- coding: utf-8 -*-
import json
import os

import pytest

import click
from click.testing import CliRunner

from boussole.cli.console_script import cli_frontend
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


# Backend default filename shortcuts
YAML_FILENAME = SettingsBackendYaml._default_filename
JSON_FILENAME = SettingsBackendJson._default_filename


def test_001(settings, caplog):
    """cli.startproject: Basic"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        sourcedir = os.path.join(test_cwd, "scss")
        targetdir = os.path.join(test_cwd, "css")
        config_filepath = os.path.join(test_cwd, JSON_FILENAME)

        opts = [
            'startproject',
            '--basedir={}'.format(test_cwd),
            '--config={}'.format(JSON_FILENAME),
            '--sourcedir={}'.format("scss"),
            '--targetdir={}'.format("css"),
        ]

        # Execute command with opts
        result = runner.invoke(cli_frontend, opts)

        # Command stop on success exit code
        assert result.exit_code == 0

        # Validate return log output
        assert caplog.record_tuples == [
            (
                'boussole',
                20,
                "Project directory structure and configuration file have been created."
            ),
            (
                'boussole',
                20,
                "Now you should start to create some Sass sources into '{}', then compile them using:".format(sourcedir)
            ),
            (
                'boussole',
                20,
                '    boussole compile --config={}'.format(config_filepath)
            ),
        ]

        # Ensure dir and file has been created
        assert os.path.exists(config_filepath)
        assert os.path.exists(sourcedir)
        assert os.path.exists(targetdir)

        # Validate created configuration file
        with open(config_filepath, "r") as fp:
            assert json.load(fp) == {
                'SOURCES_PATH': 'scss',
                'TARGET_PATH': 'css',
                "LIBRARY_PATHS": [],
                "OUTPUT_STYLES": "nested",
                "SOURCE_COMMENTS": False,
                "EXCLUDES": []
            }


def test_002(settings, caplog):
    """cli.startproject: Error from given arguments (multiple identical
       paths)"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        sourcedir = os.path.join(test_cwd, "css")
        targetdir = os.path.join(test_cwd, "css")
        config_filepath = os.path.join(test_cwd, JSON_FILENAME)

        opts = [
            'startproject',
            '--basedir={}'.format(test_cwd),
            '--config={}'.format(JSON_FILENAME),
            '--sourcedir={}'.format("css"),
            '--targetdir={}'.format("css"),
        ]

        # Execute command with opts
        result = runner.invoke(cli_frontend, opts)

        # Command stop on success exit code
        assert result.exit_code == 1

        # Validate return log output
        assert caplog.record_tuples == [
            (
                'boussole',
                50,
                'Multiple occurences finded for path: {}'.format(sourcedir)
            )
        ]
