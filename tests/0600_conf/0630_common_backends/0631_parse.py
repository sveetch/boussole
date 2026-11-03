# -*- coding: utf-8 -*-
import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


@pytest.mark.parametrize("backend_engine", [
    SettingsBackendJson,
    SettingsBackendYaml,
])
def test_ok(settings, sample_project_settings, backend_engine):
    """
    Backend content parsing success
    """
    backend = backend_engine(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath()
    filepath = backend.check_filepath(path, filename)

    content = backend.open(filepath)

    assert backend.parse(filepath, content) == sample_project_settings


@pytest.mark.parametrize("filename,backend_engine", [
    ("boussole_error.json", SettingsBackendJson),
    ("boussole_error.yml", SettingsBackendYaml),
])
def test_error(settings, sample_project_settings, filename, backend_engine):
    """
    Backend content parsing error
    """
    backend = backend_engine(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath(filepath=filename)
    filepath = backend.check_filepath(path, filename)

    content = backend.open(filepath)

    with pytest.raises(SettingsBackendError):
        backend.parse(filepath, content)
