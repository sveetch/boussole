# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf import DEFAULT_SETTINGS, Settings
from boussole.conf.json_backend import SettingsLoaderJson


def test_conf_settings_update_001_basic(settings, sample_project_settings):
    """conf.Settings: Create a Settings object and fill it from loaded JSON
       settings file"""
    settings_loader = SettingsLoaderJson()
    loaded = settings_loader.load(settings.fixtures_path)

    settings_object = Settings()
    settings_object.update(loaded)

    assert settings_object._settings == sample_project_settings

    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == sample_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == sample_project_settings['COMPILER_ARGS']
    

def test_conf_settings_update_002_poluted(settings, sample_project_settings):
    """conf.Settings: Create a Settings object and fill it from loaded polluted
       JSON settings file"""
    settings_loader = SettingsLoaderJson()
    loaded = settings_loader.load(settings.fixtures_path, filename="settings_polluted.json")

    settings_object = Settings()
    settings_object.update(loaded)

    assert settings_object._settings == sample_project_settings

    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == sample_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == sample_project_settings['COMPILER_ARGS']
    
    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None
    

def test_conf_settings_update_003_custom(settings, custom_project_settings):
    """conf.Settings: Create a Settings object and fill it from loaded custom
       JSON settings file"""
    settings_loader = SettingsLoaderJson()
    loaded = settings_loader.load(settings.fixtures_path, filename="settings_custom.json")

    settings_object = Settings()
    settings_object.update(loaded)

    assert settings_object._settings == custom_project_settings

    assert settings_object.TARGET_PATH == custom_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == custom_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == custom_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == custom_project_settings['COMPILER_ARGS']
    
    # Wrong settings that does not exist and should have been removed
    assert getattr(settings_object, 'FOO', None) == None
    assert getattr(settings_object, 'BAR', None) == None
