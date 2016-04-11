# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.base_backend import SettingsBackendBase


def test_ok_001(settings):
    """conf.base_backendSettingsBackendBase: Filepath check case 1"""
    backend = SettingsBackendBase()

    result = backend.check_filepath(settings.fixtures_path, filename=SettingsBackendBase._default_filename)

    assert result == os.path.join(settings.fixtures_path, SettingsBackendBase._default_filename)


def test_ok_002(settings):
    """conf.base_backendSettingsBackendBase: Filepath check case 2"""
    backend = SettingsBackendBase()

    result = backend.check_filepath(settings.sample_path, filename="dummy")

    assert result == os.path.join(settings.sample_path, "dummy")


def test_error_001(settings):
    """conf.base_backendSettingsBackendBase: Filepath check error case 1 (dont exist)"""
    backend = SettingsBackendBase()

    with pytest.raises(SettingsBackendError):
        backend.check_filepath(settings.fixtures_path, filename="dontexists")


def test_error_002(settings):
    """conf.base_backendSettingsBackendBase: Filepath check error case 2 (filename is a dir)"""
    backend = SettingsBackendBase()

    with pytest.raises(SettingsBackendError):
        backend.check_filepath(settings.sample_path, filename="components")
