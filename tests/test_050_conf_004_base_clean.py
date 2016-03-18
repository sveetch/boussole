# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.base_backend import SettingsLoaderBase


def test_settings_base_clean_001(settings, sample_project_settings):
    """conf.base_backendSettingsLoaderBase: Ensure cleaning dont drop anything"""
    settings_loader = SettingsLoaderBase()
    
    assert settings_loader.clean(sample_project_settings) == sample_project_settings
