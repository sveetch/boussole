# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.model import Settings
from boussole.conf.json_backend import SettingsBackendJson


def test_conf_settings_load_001_basic(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: Load basic JSON settings file"""
    settings_loader = SettingsBackendJson(basedir=settings.fixtures_path)

    settings_object = settings_loader.load()

    assert settings_object._settings == sample_project_settings

    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == sample_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == sample_project_settings['COMPILER_ARGS']


def test_conf_settings_load_002_poluted(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: Load polluted JSON settings
       file"""
    settings_loader = SettingsBackendJson(basedir=settings.fixtures_path)

    settings_object = settings_loader.load(filename="settings_polluted.json")

    assert settings_object._settings == sample_project_settings

    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == sample_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == sample_project_settings['COMPILER_ARGS']

    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None


def test_conf_settings_load_003_custom(settings, custom_project_settings):
    """conf.json_backend.SettingsBackendJson: Load custom JSON settings file"""
    settings_loader = SettingsBackendJson(basedir=settings.fixtures_path)

    settings_object = settings_loader.load(filename="settings_custom.json")

    assert settings_object._settings == custom_project_settings

    assert settings_object.TARGET_PATH == custom_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == custom_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == custom_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == custom_project_settings['COMPILER_ARGS']

    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None
