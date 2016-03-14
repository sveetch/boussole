# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import SettingsLoadingError
from boussole.conf.base_backend import SettingsLoaderBase


def test_settings_base_filepath_ok_001(settings):
    """conf.base_backendSettingsLoaderBase: Filepath check case 1"""
    settings_loader = SettingsLoaderBase()
    
    settings_loader.get_filepath(settings.sample_path)


def test_settings_base_filepath_ok_002(settings):
    """conf.base_backendSettingsLoaderBase: Filepath check case 2"""
    settings_loader = SettingsLoaderBase()
    
    settings_loader.get_filepath(settings.sample_path, filename="dummy")


def test_settings_base_filepath_error_001(settings):
    """conf.base_backendSettingsLoaderBase: Filepath check error case 1 (dont exist)"""
    settings_loader = SettingsLoaderBase()
    
    with pytest.raises(SettingsLoadingError):
        settings_loader.get_filepath(settings.sample_path, filename="dontexists")


def test_settings_base_filepath_error_002(settings):
    """conf.base_backendSettingsLoaderBase: Filepath check error case 2 (filename is a dir)"""
    settings_loader = SettingsLoaderBase()
    
    with pytest.raises(SettingsLoadingError):
        settings_loader.get_filepath(settings.sample_path, filename="components")
