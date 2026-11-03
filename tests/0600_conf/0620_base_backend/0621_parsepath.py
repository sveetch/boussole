# -*- coding: utf-8 -*-
import pytest

from boussole.conf.base_backend import SettingsBackendBase


@pytest.mark.parametrize("settings_kwargs,parse_kwargs,expected", [
    # no path given and with empty basedir
    (
        {},
        {},
        (".", "boussole.txt"),
    ),
    # no path given and with a basedir
    (
        {"basedir": "/home/bart/www"},
        {},
        ("/home/bart/www", "boussole.txt"),
    ),
    # filename and empty basedir
    (
        {},
        {"filepath": "boussole_custom.txt"},
        (".", "boussole_custom.txt"),
    ),
    # filename and filled basedir
    (
        {"basedir": "/home/bart/www"},
        {"filepath": "boussole_custom.txt"},
        ("/home/bart/www", "boussole_custom.txt"),
    ),
    # relative filepath and empty basedir
    (
        {},
        {"filepath": "foo/boussole_custom.txt"},
        ("foo", "boussole_custom.txt"),
    ),
    # relative filepath and filled basedir
    (
        {"basedir": "/home/bart/www"},
        {"filepath": "foo/boussole_custom.txt"},
        ("/home/bart/www/foo", "boussole_custom.txt"),
    ),
    # absolute filepath and empty basedir
    (
        {},
        {"filepath": "/home/bart/www/boussole_custom.txt"},
        ("/home/bart/www", "boussole_custom.txt"),
    ),
    # absolute filepath and filled basedir to ensure basedir is ignored with
    # absolute filepath
    (
        {"basedir": "/home/no/pasaran"},
        {"filepath": "/home/bart/www/boussole_custom.txt"},
        ("/home/bart/www", "boussole_custom.txt"),
    ),
    # filename and filled basedir, need normalize
    (
        {"basedir": "/home/bart/www"},
        {"filepath": "./boussole_custom.txt"},
        ("/home/bart/www", "boussole_custom.txt"),
    ),
    # filename and filled basedir, need normalize
    (
        {"basedir": "/home/bart/www"},
        {"filepath": "../boussole_custom.txt"},
        ("/home/bart", "boussole_custom.txt"),
    ),
    # filename and empty basedir, normalize can't do anything
    (
        {},
        {"filepath": "../boussole_custom.txt"},
        ("..", "boussole_custom.txt"),
    ),
])
def test_base_parsepath(settings, sample_project_settings, settings_kwargs,
                        parse_kwargs, expected):
    """
    no path given and with empty basedir
    """
    backend = SettingsBackendBase(**settings_kwargs)

    result = backend.parse_filepath(**parse_kwargs)

    assert result == expected
