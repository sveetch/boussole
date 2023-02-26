# -*- coding: utf-8 -*-
import json
import os
import pyaml

import pytest

from click.testing import CliRunner

from boussole.cli.console_script import cli_frontend
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


# Backend default filename shortcuts
YAML_FILENAME = SettingsBackendYaml._default_filename
JSON_FILENAME = SettingsBackendJson._default_filename


@pytest.mark.parametrize("options,filename", [
    ([], JSON_FILENAME),
    (["--backend=yaml"], YAML_FILENAME),
    (["--backend=json"], JSON_FILENAME),
])
def test_error_verbosity_001(caplog, options, filename):
    """
    Testing default verbosity (aka INFO level) on setting error with
    different backends
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Default verbosity
        result = runner.invoke(cli_frontend, ["compile"]+options)

        assert result.exit_code == 1

        assert caplog.record_tuples == [
            (
                "boussole",
                20,
                "Building project"
            ),
            (
                "boussole",
                50,
                "Unable to find any settings in directory: {}".format(test_cwd)
            )
        ]

        assert "Aborted!" in result.output


def test_error_verbosity_002(caplog):
    """
    Testing silent on setting error
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Silent
        result = runner.invoke(cli_frontend, ["-v 0", "compile"])

        error_msg = "Unable to find any settings in directory: {}".format(
            test_cwd
        )

        assert result.exit_code == 1

        assert caplog.record_tuples == [
            (
                "boussole",
                50,
                error_msg
            )
        ]

        # Totally silent output excepted the one from click.Abort()
        assert error_msg not in result.output
        assert "Aborted!" in result.output


def test_error_verbosity_003(caplog):
    """
    Testing debug level verbosity on setting error
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Silent
        result = runner.invoke(cli_frontend, ["-v 5", "compile"])

        error_msg = "Unable to find any settings in directory: {}".format(
            test_cwd
        )

        assert result.exit_code == 1

        assert caplog.record_tuples == [
            (
                "boussole",
                20,
                "Building project"
            ),
            (
                "boussole",
                50,
                error_msg
            )
        ]
        assert error_msg in result.output
        assert "Aborted!" in result.output


def test_error_verbosity_004(caplog):
    """
    Testing debug level verbosity on some file to compile
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Need a file to compile, as setting error is not really verbose
        # Write a minimal config file
        with open(JSON_FILENAME, "w") as f:
            f.write(json.dumps({
                "SOURCES_PATH": ".",
                "TARGET_PATH": "./css",
                "OUTPUT_STYLES": "compact",
            }, indent=4))
        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main Sass source
        source = "\n".join((
            """/* Main sample */""",
            """#content{""",
            """    color: red;""",
        ))
        with open("main.scss", "w") as f:
            f.write(source)

        # Silent
        result = runner.invoke(cli_frontend, ["-v 5", "compile"])

        error_msg = (
            "Error: Invalid CSS after \"    color: red;\": expected \"}\", "
            "was \"\"\n        on line 3:15 of main.scss\n>>     "
            "color: red;\n   --------------^\n"
        )

        assert result.exit_code == 1
        assert caplog.record_tuples == [
            (
                "boussole",
                20,
                "Building project"
            ),
            (
                "boussole",
                10,
                "Settings file: {}/{} (json)".format(test_cwd, JSON_FILENAME)
            ),
            (
                "boussole",
                10,
                "Project sources directory: {}".format(test_cwd)
            ),
            (
                "boussole",
                10,
                "Project destination directory: {}/css".format(test_cwd)
            ),
            (
                "boussole",
                10,
                "Exclude patterns: []"
            ),
            (
                "boussole",
                10,
                "Compile: {}/main.scss".format(test_cwd)
            ),
            (
                "boussole",
                40,
                error_msg
            )
        ]
        assert error_msg in result.output
        assert "Aborted!" in result.output


def test_fail_001():
    """
    Testing basic compile fail on default config filename (does not exists)
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        result = runner.invoke(cli_frontend, ["compile"])

        assert result.exit_code == 1
        assert "Aborted!" in result.output


def test_fail_002():
    """
    Testing basic compile fail on given path directory (not a filename) as
    config file
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        config_arg = "--config={}".format(test_cwd)

        result = runner.invoke(cli_frontend, ["compile", config_arg])

        assert result.exit_code == 1
        assert "Aborted!" in result.output


def test_fail_003():
    """
    Testing basic compile fail on invalid config file (invalid JSON)
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        with open(JSON_FILENAME, "w") as f:
            f.write("Invalid settings file content")

        result = runner.invoke(cli_frontend, ["compile"])

        msg = """No JSON object could be decoded from file: {}/{}"""
        assert result.exit_code == 1
        assert msg.format(test_cwd, JSON_FILENAME) in result.output
        assert "Aborted!" in result.output


def test_fail_004():
    """
    Testing exceptions management from sass compiler on invalid syntax
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Write a minimal config file
        with open(JSON_FILENAME, "w") as f:
            f.write(json.dumps({
                "SOURCES_PATH": ".",
                "TARGET_PATH": "./css",
                "OUTPUT_STYLES": "compact",
            }, indent=4))

        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main Sass source
        source = "\n".join((
            """/* Main sample */""",
            """#content{""",
            """    color: red;""",
        ))
        with open("main.scss", "w") as f:
            f.write(source)

        # Invoke command action
        result = runner.invoke(cli_frontend, ["compile"])

        msg = """Invalid CSS after "    color: red;": expected "}", was """""

        assert result.exit_code == 1
        assert msg in result.output
        assert "Aborted!" in result.output


def test_fail_005():
    """
    Testing exceptions management from core API
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Write a minimal config file
        with open(JSON_FILENAME, "w") as f:
            f.write(json.dumps({
                "SOURCES_PATH": ".",
                "TARGET_PATH": "./css",
                "OUTPUT_STYLES": "compact",
            }, indent=4))

        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main Sass source
        source = "\n".join((
            """/* Main sample */""",
            """@import "mip";""",
        ))
        with open("main.scss", "w") as f:
            f.write(source)

        # Invoke command action
        result = runner.invoke(cli_frontend, ["compile"])

        msg = """File to import not found or unreadable: mip"""

        assert result.exit_code == 1
        assert msg in result.output
        assert "Aborted!" in result.output


@pytest.mark.parametrize("options,filename,dumper", [
    ([], JSON_FILENAME, json.dump),
    (["--backend=yaml"], YAML_FILENAME, pyaml.dump),
    (["--backend=json"], JSON_FILENAME, json.dump),
])
def test_success_basic(options, filename, dumper):
    """
    Testing compile success on basic config, a main Sass source and a partial
    source to ignore and mixed Sass format (imported sass source from scss)
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()

        # Write a minimal config file
        with open(filename, "w") as f:
            datas = {
                "SOURCES_PATH": ".",
                "TARGET_PATH": "./css",
                "OUTPUT_STYLES": "compact",
                "SOURCE_MAP": True,
            }
            dumper(datas, f, indent=4)

        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main scss source
        source = "\n".join((
            """/* Main scss sample */""",
            """#content{""",
            """    color: red;""",
            """    &.wide{""",
            """        margin: 50px 15px;""",
            """    }""",
            """}""",
            """@import "sass_addon";""",
        ))
        with open("main.scss", "w") as f:
            f.write(source)

        # Write a minimal main scss source
        source = "\n".join((
            """/* sass addon */""",
            """#sass-addon""",
            """    color: blue""",
        ))
        with open("_sass_addon.sass", "w") as f:
            f.write(source)

        # Write a partial Sass source
        source = "\n".join((
            """/* Partial source to ignore */""",
            """.toignore-partial{""",
            """    color: gold !important;""",
            """}""",
        ))
        with open("_toignore.scss", "w") as f:
            f.write(source)

        # Invoke command action
        result = runner.invoke(cli_frontend, ["compile"]+options)

        # Attempted compiled CSS
        expected_css = "\n".join((
            """/* Main scss sample */""",
            """#content { color: red; }""",
            "",
            """#content.wide { margin: 50px 15px; }""",
            "",
            """/* sass addon */""",
            """#sass-addon { color: blue; }""",
            "",
            """/*# sourceMappingURL=main.map */""",
        ))
        with open(os.path.join(test_cwd, "css", "main.css"), "r") as f:
            compiled_css = f.read()

        # Command success signal exit
        assert result.exit_code == 0
        # Source is correctly compiled
        assert compiled_css == expected_css
        # Partial source to ignore is ignored
        results = os.listdir(os.path.join(test_cwd, "css"))
        results.sort()
        assert results == [
            "main.css",
            "main.map",
        ]


@pytest.mark.parametrize("options,filename,dumper", [
    ([], JSON_FILENAME, json.dump),
    (["--backend=yaml"], YAML_FILENAME, pyaml.dump),
    (["--backend=json"], JSON_FILENAME, json.dump),
])
def test_success_hash(caplog, options, filename, dumper):
    """
    Testing compile success on basic config with hash suffix enabled should produce
    CSS files with a hash in filename.
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        print(test_cwd)

        # Write a minimal config file
        with open(filename, "w") as f:
            datas = {
                "SOURCES_PATH": ".",
                "TARGET_PATH": "./css",
                "OUTPUT_STYLES": "compact",
                "SOURCE_MAP": True,
                "HASH_SUFFIX": "dummy-hash",
            }
            dumper(datas, f, indent=4)

        # Create needed dirs
        os.makedirs(os.path.join(test_cwd, "css"))

        # Write a minimal main scss source
        source = "\n".join((
            """/* Main scss sample */""",
            """#content{""",
            """    color: red;""",
            """    &.wide{""",
            """        margin: 50px 15px;""",
            """    }""",
            """}""",
        ))
        with open("main.scss", "w") as f:
            f.write(source)

        # Invoke command action
        result = runner.invoke(cli_frontend, ["-v 5", "compile"] + options)

        # Attempted compiled CSS
        expected_css = "\n".join((
            """/* Main scss sample */""",
            """#content { color: red; }""",
            "",
            """#content.wide { margin: 50px 15px; }""",
            "",
            """/*# sourceMappingURL=main.dummy-hash.map */""",
        ))
        with open(os.path.join(test_cwd, "css", "main.dummy-hash.css"), "r") as f:
            compiled_css = f.read()

        # Command success signal exit
        assert result.exit_code == 0
        # Source is correctly compiled
        assert compiled_css == expected_css
        # Partial source to ignore is ignored
        results = os.listdir(os.path.join(test_cwd, "css"))
        results.sort()
        assert results == [
            "main.dummy-hash.css",
            "main.dummy-hash.map",
        ]
