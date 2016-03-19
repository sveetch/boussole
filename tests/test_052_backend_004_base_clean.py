# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.base_backend import SettingsBackendBase


def test_settings_base_clean_001(settings, sample_project_settings):
    """conf.base_backend.SettingsBackendBase: Ensure cleaning dont drop anything"""
    settings_loader = SettingsBackendBase()
    
    assert settings_loader.clean(sample_project_settings) == sample_project_settings
