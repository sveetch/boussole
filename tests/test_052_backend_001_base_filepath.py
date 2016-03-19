# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.base_backend import SettingsBackendBase


def test_settings_base_filepath_ok_001(settings):
    """conf.base_backendSettingsBackendBase: Filepath check case 1"""
    settings_loader = SettingsBackendBase()
    
    result = settings_loader.get_filepath(settings.fixtures_path)
    
    assert result == os.path.join(settings.fixtures_path, SettingsBackendBase._default_filename)


def test_settings_base_filepath_ok_002(settings):
    """conf.base_backendSettingsBackendBase: Filepath check case 2"""
    settings_loader = SettingsBackendBase()
    
    result = settings_loader.get_filepath(settings.sample_path, filename="dummy")
    
    assert result == os.path.join(settings.sample_path, "dummy")


def test_settings_base_filepath_error_001(settings):
    """conf.base_backendSettingsBackendBase: Filepath check error case 1 (dont exist)"""
    settings_loader = SettingsBackendBase()
    
    with pytest.raises(SettingsBackendError):
        settings_loader.get_filepath(settings.fixtures_path, filename="dontexists")


def test_settings_base_filepath_error_002(settings):
    """conf.base_backendSettingsBackendBase: Filepath check error case 2 (filename is a dir)"""
    settings_loader = SettingsBackendBase()
    
    with pytest.raises(SettingsBackendError):
        settings_loader.get_filepath(settings.sample_path, filename="components")
