# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf.base_backend import SettingsBackendBase


def test_ok_001(settings):
    """conf.base_backend.SettingsBackendBase: Dummy content parsing"""
    backend = SettingsBackendBase(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath()
    filepath = backend.check_filepath(path, filename)

    content = backend.open(filepath)

    assert backend.parse(filepath, content) == {}
