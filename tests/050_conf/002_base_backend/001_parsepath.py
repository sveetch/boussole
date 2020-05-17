# -*- coding: utf-8 -*-
from boussole.conf.base_backend import SettingsBackendBase


def test_001_empty_nobasedir(settings, sample_project_settings):
    """
    no path given and with empty basedir
    """
    backend = SettingsBackendBase()

    result = backend.parse_filepath()

    assert result == (
        '.',
        "settings.txt"
    )


def test_002_empty_basedir(settings, sample_project_settings):
    """
    no path given and with a basedir
    """
    backend = SettingsBackendBase(basedir="/home/bart/www")

    result = backend.parse_filepath()

    assert result == (
        "/home/bart/www",
        "settings.txt"
    )


def test_003_filename_nobasedir(settings, sample_project_settings):
    """
    filename and empty basedir
    """
    backend = SettingsBackendBase()

    result = backend.parse_filepath(filepath="settings_custom.txt")

    assert result == (
        '.',
        "settings_custom.txt",
    )


def test_004_filename_basedir(settings, sample_project_settings):
    """
    filename and filled basedir
    """
    backend = SettingsBackendBase(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="settings_custom.txt")

    assert result == (
        '/home/bart/www',
        "settings_custom.txt",
    )


def test_005_relative_nobasedir(settings, sample_project_settings):
    """
    relative filepath and empty basedir
    """
    backend = SettingsBackendBase()

    result = backend.parse_filepath(filepath="foo/settings_custom.txt")

    assert result == (
        'foo',
        "settings_custom.txt",
    )


def test_006_relative_basedir(settings, sample_project_settings):
    """
    relative filepath and filled basedir
    """
    backend = SettingsBackendBase(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="foo/settings_custom.txt")

    assert result == (
        "/home/bart/www/foo",
        "settings_custom.txt",
    )


def test_007_absolute_nobasedir(settings, sample_project_settings):
    """
    absolute filepath and empty basedir
    """
    backend = SettingsBackendBase()

    result = backend.parse_filepath(filepath="/home/bart/www/settings_custom.txt")

    assert result == (
        "/home/bart/www",
        "settings_custom.txt",
    )


def test_008_absolute_basedir(settings, sample_project_settings):
    """
    absolute filepath and filled basedir to ensure basedir is ignored with
    absolute filepath
    """
    backend = SettingsBackendBase(basedir="/home/no/pasaran")

    result = backend.parse_filepath(filepath="/home/bart/www/settings_custom.txt")

    assert result == (
        "/home/bart/www",
        "settings_custom.txt",
    )


def test_010_normalize_01_basedir(settings, sample_project_settings):
    """
    filename and filled basedir, need normalize
    """
    backend = SettingsBackendBase(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="./settings_custom.txt")

    assert result == (
        '/home/bart/www',
        "settings_custom.txt",
    )


def test_009_normalize_02_basedir(settings, sample_project_settings):
    """
    filename and filled basedir, need normalize
    """
    backend = SettingsBackendBase(basedir="/home/bart/www")

    result = backend.parse_filepath(filepath="../settings_custom.txt")

    assert result == (
        '/home/bart',
        "settings_custom.txt",
    )


def test_011_normalize_nobasedir(settings, sample_project_settings):
    """
    filename and empty basedir, normalize can't do anything
    """
    backend = SettingsBackendBase()

    result = backend.parse_filepath(filepath="../settings_custom.txt")

    assert result == (
        '..',
        "settings_custom.txt",
    )
