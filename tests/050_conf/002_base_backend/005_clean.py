# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.base_backend import SettingsBackendBase


def test_001(settings, custom_project_settings):
    """conf.base_backend.SettingsBackendBase: Ensure cleaning dont drop anything"""
    backend = SettingsBackendBase(basedir=settings.fixtures_path)

    assert backend.clean(custom_project_settings) == custom_project_settings
