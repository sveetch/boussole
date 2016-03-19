# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf import DEFAULT_SETTINGS
from boussole.conf.model import Settings


def test_conf_settings_init_001_default(settings, sample_project_settings):
    """conf.Settings: Create a empty Settings object width default values"""
    settings_object = Settings()

    assert settings_object._settings == DEFAULT_SETTINGS

    assert settings_object.TARGET_PATH == DEFAULT_SETTINGS['TARGET_PATH']
    assert settings_object.COMPILER_ARGS == DEFAULT_SETTINGS['COMPILER_ARGS']
