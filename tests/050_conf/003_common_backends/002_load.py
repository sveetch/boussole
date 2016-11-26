# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.exceptions import SettingsInvalidError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


@pytest.mark.parametrize("backend_engine", [
    SettingsBackendJson,
    SettingsBackendYaml,
])
def test_basic(settings, custom_project_settings, backend_engine):
    """Load basic settings file fail because of wrong paths"""
    backend = backend_engine(basedir=settings.fixtures_path)

    with pytest.raises(SettingsInvalidError):
        settings_object = backend.load()


@pytest.mark.parametrize("filename,backend_engine", [
    ("settings_polluted.json", SettingsBackendJson),
    ("settings_custom.json", SettingsBackendJson),
    ("settings_polluted.yml",SettingsBackendYaml),
    ("settings_custom.yml", SettingsBackendYaml),
])
def test_polluted(settings, custom_project_settings, filename,
                      backend_engine):
    """Load polluted settings file"""
    backend = backend_engine(basedir=settings.fixtures_path)

    settings_object = backend.load(filepath=filename)

    assert settings_object._settings == custom_project_settings

    assert settings_object.TARGET_PATH == custom_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATH == custom_project_settings['SOURCES_PATH']
    assert settings_object.LIBRARY_PATHS == custom_project_settings['LIBRARY_PATHS']
    assert settings_object.OUTPUT_STYLES == custom_project_settings['OUTPUT_STYLES']

    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None


@pytest.mark.parametrize("filename,backend_engine", [
    ("settings_custom.json", SettingsBackendJson),
    ("settings_custom.yml", SettingsBackendYaml),
])
def test_custom(settings, custom_project_settings, filename,
                    backend_engine):
    """Load custom settings file with basedir and relative filepath"""
    backend = backend_engine(basedir=settings.tests_path)

    filepath = os.path.join(settings.fixtures_dir, filename)

    settings_object = backend.load(filepath=filepath)

    assert settings_object._settings == custom_project_settings
