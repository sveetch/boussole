# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf.base_backend import SettingsLoaderBase


def test_settings_base_open_ok_001(settings):
    """conf.base_backend.SettingsLoaderBase: Open given filepath"""
    settings_loader = SettingsLoaderBase()
    
    filepath = settings_loader.get_filepath(settings.sample_path)
    
    assert settings_loader.open(filepath) == """Fake settings file as SettingsLoaderBase dont implement a full usable interface."""
