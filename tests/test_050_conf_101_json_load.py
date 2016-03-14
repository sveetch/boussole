# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.json_backend import SettingsLoaderJson


def test_settings_base_load_ok_001(settings, sample_project_settings):
    """conf.json_backend.SettingsLoaderJson: Load basic JSON settings file"""
    settings_loader = SettingsLoaderJson()
    
    loaded = settings_loader.load(settings.sample_path)
    
    assert loaded == sample_project_settings


def test_settings_base_load_ok_002(settings, sample_project_settings):
    """conf.json_backend.SettingsLoaderJson: Load custom JSON settings file"""
    settings_loader = SettingsLoaderJson()
    
    loaded = settings_loader.load(settings.sample_path, filename="settings_custom.json")
    
    custom_settings = copy.deepcopy(sample_project_settings)
    
    # Add custom elements to sample settings
    custom_settings.update({
        "TARGAT_PATH": "/home/bar",
        "BAR": [
            "meep",
            "meep"
        ],
        "FOO": 42
    })
    
    assert loaded == custom_settings
