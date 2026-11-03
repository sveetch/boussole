import json

from click.testing import CliRunner

from boussole.cli.console_script import cli_frontend
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


# Backend default filename shortcuts
YAML_FILENAME = SettingsBackendYaml._default_filename
JSON_FILENAME = SettingsBackendJson._default_filename


def test_basic(settings, caplog, tmp_path):
    """
    Basic usage of startproject should just work correctly and create structure with
    correct config.
    """
    runner = CliRunner()

    sourcedir = tmp_path / "scss"
    targetdir = tmp_path / "css"
    config_filepath = tmp_path / JSON_FILENAME

    opts = [
        "startproject",
        "--basedir", tmp_path,
        "--backend", "json",
        "--config", JSON_FILENAME,
        "--sourcedir", "scss",
        "--targetdir", "css",
    ]

    # Execute command with opts
    result = runner.invoke(cli_frontend, opts)

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
    assert config_filepath.exists() is True
    assert sourcedir.exists() is True
    assert targetdir.exists() is True

    # Validate created configuration file
    assert json.loads(config_filepath.read_text()) == {
        "SOURCES_PATH": "scss",
        "TARGET_PATH": "css",
        "LIBRARY_PATHS": [],
        "OUTPUT_STYLES": "nested",
        "HASH_SUFFIX": None,
        "SOURCE_COMMENTS": False,
        "EXCLUDES": []
    }


def test_identical_source_target(settings, caplog, tmp_path):
    """
    Error from given arguments (multiple identical paths)
    """
    runner = CliRunner()

    sourcedir = tmp_path / "css"

    opts = [
        "startproject",
        "--basedir", tmp_path,
        "--backend", "json",
        "--config", JSON_FILENAME,
        "--sourcedir", "css",
        "--targetdir", "css",
    ]

    # Execute command with opts
    result = runner.invoke(cli_frontend, opts)

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
