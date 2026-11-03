# -*- coding: utf-8 -*-
import json
import os

from click.testing import CliRunner

from boussole.cli.console_script import cli_frontend
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


# Backend default filename shortcuts
YAML_FILENAME = SettingsBackendYaml._default_filename
JSON_FILENAME = SettingsBackendJson._default_filename

def debug_click_invoke(result, caplog=None):
    """
    Output important informations on Click invoke result and optionally caplog.

    It invoke command has raised an exception, raise it up.
    """
    print("=> result.output <=")
    print(result.output)
    print()

    if caplog:
        print("=> caplog.record_tuples <=")
        print(caplog.record_tuples)
        print()

    print("=> result.exception <=")
    print(result.exception)
    if result.exception is not None:
        raise result.exception

def test_001(settings, caplog):
    """
    Basic
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        sourcedir = os.path.join(test_cwd, "scss")
        targetdir = os.path.join(test_cwd, "css")
        config_filepath = os.path.join(test_cwd, JSON_FILENAME)

        opts = [
            "startproject",
            "--basedir", test_cwd,
            "--backend", "json",
            "--config", JSON_FILENAME,
            "--sourcedir", "scss",
            "--targetdir", "css",
        ]

        # Execute command with opts
        result = runner.invoke(cli_frontend, opts)

        #temp
        print("💸")
        debug_click_invoke(result, caplog=caplog)

        # Command stop on success exit code
        assert result.exit_code == 0

        # Validate return log output
        assert caplog.record_tuples == [
            (
                "boussole",
                20,
                ("Project directory structure and configuration file have "
                 "been created.")
            ),
            (
                "boussole",
                20,
                ("Now you should start to create some Sass sources into '{}', "
                 "then compile them using:").format(sourcedir)
            ),
            (
                "boussole",
                20,
                "    boussole compile --config={}".format(config_filepath)
            ),
        ]

        # Ensure dir and file has been created
        assert os.path.exists(config_filepath)
        assert os.path.exists(sourcedir)
        assert os.path.exists(targetdir)

        # Validate created configuration file
        with open(config_filepath, "r") as fp:
            assert json.load(fp) == {
                "SOURCES_PATH": "scss",
                "TARGET_PATH": "css",
                "LIBRARY_PATHS": [],
                "OUTPUT_STYLES": "nested",
                "HASH_SUFFIX": None,
                "SOURCE_COMMENTS": False,
                "EXCLUDES": []
            }


def test_002(settings, caplog):
    """
    Error from given arguments (multiple identical paths)
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        sourcedir = os.path.join(test_cwd, "css")

        opts = [
            "startproject",
            "--basedir", test_cwd,
            "--backend", "json",
            "--config", JSON_FILENAME,
            "--sourcedir", "css",
            "--targetdir", "css",
        ]

        # Execute command with opts
        result = runner.invoke(cli_frontend, opts)

        #temp
        print("💸")
        debug_click_invoke(result, caplog=caplog)

        # Command stop on success exit code
        assert result.exit_code == 1

        # Validate return log output
        assert caplog.record_tuples == [
            (
                "boussole",
                50,
                "Multiple occurences finded for path: {}".format(sourcedir)
            )
        ]
