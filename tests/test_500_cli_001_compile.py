# -*- coding: utf-8 -*-
import os
import json

import pytest

import click
from click.testing import CliRunner

from boussole.cli.console_script import cli_frontend


def test_cli_compile_fail_001(settings):
    """cli.compile: Testing basic compile fail on default config filename
       (does not exists)"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        result = runner.invoke(cli_frontend, ['compile'])

        assert 'Aborted!' in result.output
        assert result.exit_code == 1


def test_cli_compile_fail_002(settings):
    """cli.compile: Testing basic compile fail on given path directory (not a
       filename) as config file"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        config_arg = '--config={}'.format(test_cwd)

        result = runner.invoke(cli_frontend, ['compile', config_arg])

        assert 'Aborted!' in result.output
        assert result.exit_code == 1


def test_cli_compile_fail_003(settings):
    """cli.compile: Testing basic compile fail on invalid config file (invalid
       JSON)"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        with open('settings.json', 'w') as f:
            f.write('Invalid settings file content')

        result = runner.invoke(cli_frontend, ['compile'])

        msg = """No JSON object could be decoded from file: {}/settings.json"""
        assert msg.format(test_cwd) in result.output
        assert 'Aborted!' in result.output
        assert result.exit_code == 1


def test_cli_compile_success_001(settings):
    """cli.compile: Testing compile success on basic config, a main SASS
       source and a partial source to ignore"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Write a minimal config file
        with open('settings.json', 'w') as f:
            f.write(json.dumps({
                'SOURCES_PATH': '.',
                'TARGET_PATH': './css',
                'OUTPUT_STYLES': 'compact',
            }, indent=4))

        # Write a minimal main SASS source
        source = "\n".join((
            """/* Main sample */""",
            """#content{""",
            """    color: red;""",
            """    &.wide{""",
            """        margin: 50px 15px;""",
            """    }""",
            """}""",
        ))
        with open('main.scss', 'w') as f:
            f.write(source)

        # Write a partial SASS source
        source = "\n".join((
            """/* Partial source to ignore */""",
            """.toignore-partial{""",
            """    color: gold !important;""",
            """}""",
        ))
        with open('_toignore.scss', 'w') as f:
            f.write(source)

        # Invoke command action
        result = runner.invoke(cli_frontend, ['-vvvv', 'compile'])

        # Attempted compiled CSS
        css_attempted = "\n".join((
            """/* Main sample */""",
            """#content { color: red; }""",
            "",
            """#content.wide { margin: 50px 15px; }""",
            "",
        ))
        with open(os.path.join(test_cwd, "css", "main.css"), 'rb') as f:
            css_compiled = f.read()

        #print result.exit_code
        #print result.output
        #print type(result)
        #print os.listdir(os.path.join(test_cwd, "css"))

        # Command success signal exit
        assert result.exit_code == 0
        # Source is correctly compiled
        assert css_compiled == css_attempted
        # Partial source to ignore is ignored
        assert os.listdir(os.path.join(test_cwd, "css")) == ['main.css']
