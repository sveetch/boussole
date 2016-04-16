# -*- coding: utf-8 -*-
import os
import pytest

from boussole.conf.base_backend import SettingsBackendBase
from boussole.conf.json_backend import SettingsBackendJson


def test_001_empty_nobasedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: no path given and
       with empty basedir"""
    backend = SettingsBackendJson()

    result = backend.parse_filepath()

    assert result == (
        '.',
        "settings.json"
    )


def test_002_empty_basedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: no path given and
       with a basedir"""
    backend = SettingsBackendJson(basedir="/home/bart/www")

    result = backend.parse_filepath()

    assert result == (
        "/home/bart/www",
        "settings.json"
    )


def test_003_filename_nobasedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: filename and empty
       basedir"""
    backend = SettingsBackendJson()

    result = backend.parse_filepath(filepath="settings_custom.json")

    assert result == (
        '.',
        "settings_custom.json",
    )


def test_004_filename_basedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: filename and filled
       basedir"""
    backend = SettingsBackendJson(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="settings_custom.json")

    assert result == (
        '/home/bart/www',
        "settings_custom.json",
    )


def test_005_relative_nobasedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: relative filepath and empty
       basedir"""
    backend = SettingsBackendJson()

    result = backend.parse_filepath(filepath="foo/settings_custom.json")

    assert result == (
        'foo',
        "settings_custom.json",
    )


def test_006_relative_basedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: relative filepath and filled
       basedir"""
    backend = SettingsBackendJson(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="foo/settings_custom.json")

    assert result == (
        "/home/bart/www/foo",
        "settings_custom.json",
    )


def test_007_absolute_nobasedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: absolute filepath and empty
       basedir"""
    backend = SettingsBackendJson()

    result = backend.parse_filepath(filepath="/home/bart/www/settings_custom.json")

    assert result == (
        "/home/bart/www",
        "settings_custom.json",
    )


def test_008_absolute_basedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: absolute filepath and filled
       basedir to ensure basedir is ignored with absolute filepath"""
    backend = SettingsBackendJson(basedir="/home/no/pasaran")

    result = backend.parse_filepath(filepath="/home/bart/www/settings_custom.json")

    assert result == (
        "/home/bart/www",
        "settings_custom.json",
    )


def test_010_normalize_01_basedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: filename and filled basedir,
       need normalize"""
    backend = SettingsBackendJson(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="./settings_custom.json")

    assert result == (
        '/home/bart/www',
        "settings_custom.json",
    )


def test_009_normalize_02_basedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: filename and filled basedir,
       need normalize"""
    backend = SettingsBackendJson(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="../settings_custom.json")

    assert result == (
        '/home/bart',
        "settings_custom.json",
    )


def test_011_normalize_nobasedir(settings, sample_project_settings):
    """conf.SettingsBackendJson.parse_filepath: filename and empty basedir,
       normalize can't do anything"""
    backend = SettingsBackendJson()

    result = backend.parse_filepath(filepath="../settings_custom.json")

    assert result == (
        '..',
        "settings_custom.json",
    )
