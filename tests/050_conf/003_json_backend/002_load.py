# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.exceptions import SettingsInvalidError
from boussole.conf.json_backend import SettingsBackendJson


def test_001_basic(settings, custom_project_settings):
    """conf.json_backend.SettingsBackendJson: Load basic JSON settings file
       fail because of wrong paths"""
    backend = SettingsBackendJson(basedir=settings.fixtures_path)

    with pytest.raises(SettingsInvalidError):
        settings_object = backend.load()


def test_002_poluted(settings, custom_project_settings):
    """conf.json_backend.SettingsBackendJson: Load polluted JSON settings
       file"""
    backend = SettingsBackendJson(basedir=settings.fixtures_path)

    settings_object = backend.load(filepath="settings_polluted.json")

    assert settings_object._settings == custom_project_settings

    assert settings_object.TARGET_PATH == custom_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATH == custom_project_settings['SOURCES_PATH']
    assert settings_object.LIBRARY_PATHS == custom_project_settings['LIBRARY_PATHS']
    assert settings_object.OUTPUT_STYLES == custom_project_settings['OUTPUT_STYLES']

    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None


def test_003_custom(settings, custom_project_settings):
    """conf.json_backend.SettingsBackendJson: Load custom JSON settings file"""
    backend = SettingsBackendJson(basedir=settings.fixtures_path)

    settings_object = backend.load(filepath="settings_custom.json")

    assert settings_object._settings == custom_project_settings

    assert settings_object.TARGET_PATH == custom_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATH == custom_project_settings['SOURCES_PATH']
    assert settings_object.LIBRARY_PATHS == custom_project_settings['LIBRARY_PATHS']
    assert settings_object.OUTPUT_STYLES == custom_project_settings['OUTPUT_STYLES']

    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None


def test_004_custom(settings, custom_project_settings):
    """conf.json_backend.SettingsBackendJson: Load custom JSON settings file
       with basedir and relative filepath"""
    backend = SettingsBackendJson(basedir=settings.tests_path)

    filepath = os.path.join(settings.fixtures_dir, "settings_custom.json")

    settings_object = backend.load(filepath=filepath)

    assert settings_object._settings == custom_project_settings

    assert settings_object.TARGET_PATH == custom_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATH == custom_project_settings['SOURCES_PATH']
    assert settings_object.LIBRARY_PATHS == custom_project_settings['LIBRARY_PATHS']
    assert settings_object.OUTPUT_STYLES == custom_project_settings['OUTPUT_STYLES']

    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None
