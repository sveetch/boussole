# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.model import Settings

def test_001_basic(settings, sample_project_settings):
    """conf.Settings: Ensure dummy update is correct"""
    settings_object = Settings()

    settings_object.update(sample_project_settings)

    assert settings_object._settings == sample_project_settings


def test_002_polluted(settings, sample_project_settings):
    """conf.Settings: Ensure update filtering is done"""
    settings_object = Settings(initial=sample_project_settings)

    # Add some wrong settings
    settings_object.update({
        'PLOP': True,
        'Foo': 42,
        'BAR': [1, 5, 10]
    })

    assert settings_object._settings == sample_project_settings


def test_003_mixed(settings, sample_project_settings):
    """conf.Settings: Ensure update filtering is correct on both enabled and
       not enabled setting names"""
    settings_object = Settings(initial=sample_project_settings)

    # Add one available setting and some other wrong settings
    settings_object.update({
        'OUTPUT_STYLES': 'compressed',
        'PLOP': True,
        'Foo': 42,
        'BAR': [1, 5, 10]
    })

    # New settings reference with modified setting
    mixed = copy.deepcopy(sample_project_settings)
    mixed.update({
        'OUTPUT_STYLES': 'compressed',
    })

    assert settings_object._settings == mixed
