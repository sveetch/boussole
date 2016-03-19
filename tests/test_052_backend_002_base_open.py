# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf.base_backend import SettingsBackendBase


def test_settings_base_open_ok_001(settings):
    """conf.base_backend.SettingsBackendBase: Open given filepath"""
    settings_loader = SettingsBackendBase()
    
    filepath = settings_loader.get_filepath(settings.fixtures_path)
    
    assert settings_loader.open(filepath) == """Fake settings file as SettingsBackendBase dont implement a full usable interface."""
