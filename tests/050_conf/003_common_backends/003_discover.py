# -*- coding: utf-8 -*-
import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.discover import get_backend


@pytest.mark.parametrize("filepath,kind,name", [
    ('foo.json', None, 'json'),
    ('foo.yml', None, 'yaml'),
    ('/home/foo.json', None, 'json'),
    ('/home/json/foo.yml', None, 'yaml'),
    ('.foo', 'json', 'json'),
    ('.foo', 'json', 'json'),
    ('/home/bar/.foo', 'yaml', 'yaml'),
    ('foo.bar', 'yaml', 'yaml'),
    ('foo.json', 'yaml', 'yaml'),
])
def test_ok(filepath, kind, name):
    """Discover backend from given filename and kind"""
    backend = get_backend(filepath, kind=kind)

    assert backend._kind_name == name


@pytest.mark.parametrize("filepath,kind", [
    ('.foo', None),
    ('foo.bar', None),
    ('foo.json.bar', None),
    ('/home/bar/.foo', None),
    ('foo.json', 'wrong'),
])
def test_error(filepath, kind):
    """Error on discovering backend from given filename"""

    with pytest.raises(SettingsBackendError):
        backend = get_backend(filepath, kind=kind)
