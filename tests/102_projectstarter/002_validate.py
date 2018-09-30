# -*- coding: utf-8 -*-
import os
import json
import pytest

from boussole.exceptions import SettingsInvalidError


@pytest.mark.parametrize("paths", [
    (
        '/home/foo',
        '/home/bar',
    ),
    (
        '/home',
        '/home/bar',
        '/var/lib',
    ),
    (
        '/home',
        '/home/bar',
        '/home/bar.gif',
        '/var/lib',
    ),
])
def test_ok(projectstarter, paths):
    """validate various correct paths"""

    assert projectstarter('json').valid_paths(*paths) == True


@pytest.mark.parametrize("paths", [
    (
        '/home/foo',
        '/home/bar',
        '/home/foo',
    ),
    (
        '/home/foo',
        '/home/bar',
        '/home/foo',
        '/home/foo',
    ),
    (
        '/home/foo',
        '/home/bar',
        '/home/foo',
        '/home/bar',
    ),
    (
        '/home/foo',
        '/home/bar',
        '/home/bar',
        '/home/foo',
        '/var/lib',
        '/var/lib',
    ),
])
def test_wrong(projectstarter, paths):
    """fail on duplicated paths"""

    with pytest.raises(SettingsInvalidError):
        projectstarter('json').valid_paths(*paths)
