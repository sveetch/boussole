# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf.base_backend import SettingsBackendBase


def test_ok_001(settings):
    """conf.base_backend.SettingsBackendBase: Open given filepath"""
    backend = SettingsBackendBase(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath()
    filepath = backend.check_filepath(path, filename)

    assert backend.open(filepath) == """Fake settings file as SettingsBackendBase dont implement a full usable interface."""
