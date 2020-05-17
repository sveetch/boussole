# -*- coding: utf-8 -*-
from boussole.conf.base_backend import SettingsBackendBase


def test_ok_001(settings):
    """
    Dummy content parsing
    """
    backend = SettingsBackendBase(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath()
    filepath = backend.check_filepath(path, filename)

    content = backend.open(filepath)

    assert backend.parse(filepath, content) == {}
