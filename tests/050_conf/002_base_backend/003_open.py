# -*- coding: utf-8 -*-
from boussole.conf.base_backend import SettingsBackendBase


def test_ok_001(settings):
    """
    Open given filepath
    """
    backend = SettingsBackendBase(basedir=settings.fixtures_path)

    path, filename = backend.parse_filepath()
    filepath = backend.check_filepath(path, filename)

    assert backend.open(filepath) == (
        """Fake settings file as SettingsBackendBase dont implement a full """
        """usable interface."""
    )
