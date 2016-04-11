# -*- coding: utf-8 -*-
import os
import copy

import pytest

from boussole.conf.model import DEFAULT_SETTINGS, Settings


def test_001_default(settings, sample_project_settings):
    """conf.Settings: Create a empty Settings object width default values"""
    settings_object = Settings()

    assert settings_object._settings == DEFAULT_SETTINGS

    assert settings_object.TARGET_PATH == DEFAULT_SETTINGS['TARGET_PATH']
    assert settings_object.OUTPUT_STYLES == DEFAULT_SETTINGS['OUTPUT_STYLES']


def test_002_minimal(settings, sample_project_settings):
    """conf.Settings: Very minimalistic settings"""
    minimal_conf = {
        'SOURCES_PATH': '.',
        'TARGET_PATH': './css',
    }

    settings_object = Settings(initial=minimal_conf)

    attempted = copy.deepcopy(DEFAULT_SETTINGS)
    attempted.update(minimal_conf)

    assert settings_object._settings == attempted

    assert settings_object.TARGET_PATH == attempted['TARGET_PATH']
    assert settings_object.OUTPUT_STYLES == attempted['OUTPUT_STYLES']
