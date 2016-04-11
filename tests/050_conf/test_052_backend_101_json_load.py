# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.json_backend import SettingsBackendJson


def test_conf_backend_json_load_001_basic(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: Load basic JSON settings file"""
    backend = SettingsBackendJson(basedir=settings.fixtures_path)

    settings_object = backend.load()

    assert settings_object._settings == sample_project_settings

    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATH == sample_project_settings['SOURCES_PATH']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.OUTPUT_STYLES == sample_project_settings['OUTPUT_STYLES']


def test_conf_backend_json_load_002_poluted(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: Load polluted JSON settings
       file"""
    backend = SettingsBackendJson(basedir=settings.fixtures_path)

    settings_object = backend.load(filepath="settings_polluted.json")

    assert settings_object._settings == sample_project_settings

    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATH == sample_project_settings['SOURCES_PATH']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.OUTPUT_STYLES == sample_project_settings['OUTPUT_STYLES']

    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None


def test_conf_backend_json_load_003_custom(settings, custom_project_settings):
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


def test_conf_backend_json_load_004_custom(settings, custom_project_settings):
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
