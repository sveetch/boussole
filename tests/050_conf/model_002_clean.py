# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.model import Settings

def test_001_basic(settings, sample_project_settings):
    """conf.Settings: Ensure cleans don't drop available settings"""
    settings_object = Settings()

    fake_settings = copy.deepcopy(sample_project_settings)

    assert settings_object.clean(fake_settings) == sample_project_settings

def test_002_custom(settings, sample_project_settings):
    """conf.Settings: Filter unavailable settings"""
    settings_object = Settings()

    fake_settings = copy.deepcopy(sample_project_settings)

    # Add some dummy settings to remove
    fake_settings.update({
        'foo': True,
        'bar': 42,
        'plonk': [],
    })

    assert settings_object.clean(fake_settings) == sample_project_settings
