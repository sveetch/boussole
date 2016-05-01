# -*- coding: utf-8 -*-
import os
import json

import pytest

import click
from click.testing import CliRunner

from boussole.cli.console_script import cli_frontend


def test_verbosity_001(settings, caplog):
    """cli.compile: Testing default verbosity (aka INFO level) on setting
       error"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Default verbosity
        result = runner.invoke(cli_frontend, ['compile'])
        assert caplog.record_tuples == [
            (
                'boussole',
                20,
                'Building project'
            ),
            (
                'boussole',
                50,
                'Unable to find settings file: {}/settings.json'.format(test_cwd)
            )
        ]
        assert 'Aborted!' in result.output
        assert result.exit_code == 1


def test_verbosity_002(settings, caplog):
    """cli.compile: Testing silent on setting error"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Silent
        result = runner.invoke(cli_frontend, ['-v 0', 'compile'])

        error_msg = 'Unable to find settings file: {}/settings.json'.format(
            test_cwd
        )

        assert caplog.record_tuples == [
            (
                'boussole',
                50,
                error_msg
            )
        ]
        assert result.exit_code == 1

        # Totally silent output excepted the one from click.Abort()
        assert error_msg not in result.output
        assert 'Aborted!' in result.output

def test_verbosity_003(settings, caplog):
    """cli.compile: Testing debug level verbosity on setting error"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Silent
        result = runner.invoke(cli_frontend, ['-v 5', 'compile'])

        error_msg = 'Unable to find settings file: {}/settings.json'.format(
            test_cwd
        )

        assert caplog.record_tuples == [
            (
                'boussole',
                20,
                'Building project'
            ),
            (
                'boussole',
                50,
                error_msg
            )
        ]
        assert error_msg in result.output
        assert 'Aborted!' in result.output
        assert result.exit_code == 1


def test_verbosity_004(settings, caplog):
    """cli.compile: Testing debug level verbosity on some file to
       compile"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Need a file to compile, as setting error is not really verbose
        # Write a minimal config file
        with open('settings.json', 'w') as f:
            f.write(json.dumps({
                'SOURCES_PATH': '.',
                'TARGET_PATH': './css',
                'OUTPUT_STYLES': 'compact',
            }, indent=4))
        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main SASS source
        source = "\n".join((
            """/* Main sample */""",
            """#content{""",
            """    color: red;""",
        ))
        with open('main.scss', 'w') as f:
            f.write(source)

        # Silent
        result = runner.invoke(cli_frontend, ['-v 5', 'compile'])

        error_msg = ("Error: Invalid CSS after \"    color: red;\": expected \"}\", "
                    "was \"\"\n        on line 3 of main.scss\n>>     "
                    "color: red;\n   ---------------^\n")

        assert result.exit_code == 1
        assert caplog.record_tuples == [
            ('boussole', 20, 'Building project'),
            ('boussole', 10, 'Project sources directory: {}'.format(test_cwd)),
            ('boussole', 10, 'Project destination directory: {}/css'.format(test_cwd)),
            ('boussole', 10, 'Exclude patterns: []'),
            ('boussole', 10, 'Compile: {}/main.scss'.format(test_cwd)),
            ('boussole', 40, error_msg)
        ]
        assert error_msg in result.output
        assert 'Aborted!' in result.output


def test_fail_001(settings, caplog):
    """cli.compile: Testing basic compile fail on default config filename
       (does not exists)"""
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        result = runner.invoke(cli_frontend, ['compile'])

        assert result.exit_code == 1
        assert 'Aborted!' in result.output


def test_fail_002(settings):
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


def test_fail_003(settings, caplog):
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
        assert result.exit_code == 1
        assert msg.format(test_cwd) in result.output
        assert 'Aborted!' in result.output


def test_fail_004(settings, caplog):
    """cli.compile: Testing exceptions management from sass compiler on
       invalid syntax"""
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

        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main SASS source
        source = "\n".join((
            """/* Main sample */""",
            """#content{""",
            """    color: red;""",
        ))
        with open('main.scss', 'w') as f:
            f.write(source)

        # Invoke command action
        result = runner.invoke(cli_frontend, ['compile'])

        msg = """Invalid CSS after "    color: red;": expected "}", was """""

        assert result.exit_code == 1
        assert msg in result.output
        assert 'Aborted!' in result.output


def test_fail_005(settings, caplog):
    """cli.compile: Testing exceptions management from core API"""
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

        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main SASS source
        source = "\n".join((
            """/* Main sample */""",
            """@import "mip";""",
        ))
        with open('main.scss', 'w') as f:
            f.write(source)

        # Invoke command action
        result = runner.invoke(cli_frontend, ['compile'])

        msg = """File to import not found or unreadable: mip"""

        assert result.exit_code == 1
        assert msg in result.output
        assert 'Aborted!' in result.output


def test_success_001(settings, caplog):
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
                'SOURCE_MAP': True,
            }, indent=4))

        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

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
        result = runner.invoke(cli_frontend, ['compile'])

        # Attempted compiled CSS
        css_attempted = "\n".join((
            """/* Main sample */""",
            """#content { color: red; }""",
            "",
            """#content.wide { margin: 50px 15px; }""",
            "",
            """/*# sourceMappingURL=css/main.map */""",
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
        assert os.listdir(os.path.join(test_cwd, "css")) == ['main.map', 'main.css']
