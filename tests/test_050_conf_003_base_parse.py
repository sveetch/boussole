# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf.base_backend import SettingsLoaderBase


def test_settings_base_parse_ok_001(settings):
    """conf.base_backend.SettingsLoaderBase: Dummy content parsing"""
    settings_loader = SettingsLoaderBase()
    
    filepath = settings_loader.get_filepath(settings.sample_path)
    
    content = settings_loader.open(filepath)
    
    assert settings_loader.parse(filepath, content) == {}
