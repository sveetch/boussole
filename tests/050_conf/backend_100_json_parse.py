# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson


def test_ok_001(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: JSON content parsing"""
    backend = SettingsBackendJson(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath()
    filepath = backend.check_filepath(path, filename)

    content = backend.open(filepath)

    assert backend.parse(filepath, content) == sample_project_settings


def test_error_001(settings, sample_project_settings):
    """conf.json_backend.SettingsBackendJson: JSON content parsing error"""
    backend = SettingsBackendJson(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath(filepath="settings.txt")
    filepath = backend.check_filepath(path, filename)

    content = backend.open(filepath)

    with pytest.raises(SettingsBackendError):
        backend.parse(filepath, content)
