# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf import DEFAULT_SETTINGS, Settings
from boussole.conf.json_backend import SettingsLoaderJson


def test_conf_settings_001_default(settings, sample_project_settings):
    """conf.Settings: Create a empty Settings object width default values"""
    settings_object = Settings()
    
    assert settings_object._settings == DEFAULT_SETTINGS
    
    assert settings_object.TARGET_PATH == DEFAULT_SETTINGS['TARGET_PATH']
    assert settings_object.COMPILER_ARGS == DEFAULT_SETTINGS['COMPILER_ARGS']
    

def test_conf_settings_002_basic(settings, sample_project_settings):
    """conf.Settings: Create a Settings object and fill it from loaded JSON
       settings file"""
    settings_loader = SettingsLoaderJson()
    loaded = settings_loader.load(settings.sample_path)
    
    settings_object = Settings()
    settings_object.update(loaded)
    
    assert settings_object._settings == sample_project_settings
    
    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == sample_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == sample_project_settings['COMPILER_ARGS']
    

def test_conf_settings_003_custom(settings, sample_project_settings):
    """conf.Settings: Create a Settings object and fill it from loaded custom
       JSON settings file"""
    settings_loader = SettingsLoaderJson()
    loaded = settings_loader.load(settings.sample_path, filename="settings_custom.json")
    
    settings_object = Settings()
    settings_object.update(loaded)
    
    assert settings_object._settings == sample_project_settings
    
    assert settings_object.TARGET_PATH == sample_project_settings['TARGET_PATH']
    assert settings_object.SOURCES_PATHS == sample_project_settings['SOURCES_PATHS']
    assert settings_object.LIBRARY_PATHS == sample_project_settings['LIBRARY_PATHS']
    assert settings_object.COMPILER_ARGS == sample_project_settings['COMPILER_ARGS']
