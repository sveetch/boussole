# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson


def test_settings_base_parse_ok_001(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: JSON content parsing"""
    settings_loader = SettingsBackendJson()

    filepath = settings_loader.get_filepath(settings.fixtures_path)

    content = settings_loader.open(filepath)

    assert settings_loader.parse(filepath, content) == sample_project_settings


def test_settings_base_parse_error_001(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: JSON content parsing error"""
    settings_loader = SettingsBackendJson()

    filepath = settings_loader.get_filepath(settings.fixtures_path, "settings.txt")

    content = settings_loader.open(filepath)

    with pytest.raises(SettingsBackendError):
        settings_loader.parse(filepath, content)
