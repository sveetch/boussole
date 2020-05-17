# -*- coding: utf-8 -*-
from boussole.conf.base_backend import SettingsBackendBase


def test_001(settings, custom_project_settings):
    """
    Ensure cleaning dont drop anything
    """
    backend = SettingsBackendBase(basedir=settings.fixtures_path)

    assert backend.clean(custom_project_settings) == custom_project_settings
