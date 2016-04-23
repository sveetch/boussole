# -*- coding: utf-8 -*-
import os
import json
import pytest

from boussole.exceptions import SettingsInvalidError


def test_ok_001(projectstarter):
    """project.valid_paths: correct paths"""

    assert projectstarter.valid_paths(*(
        '/home/foo',
        '/home/bar',
    )) == True


def test_ok_002(projectstarter):
    """project.valid_paths: correct paths"""

    assert projectstarter.valid_paths(*(
        '/home',
        '/home/bar',
        '/var/lib',
    )) == True


def test_ok_003(projectstarter):
    """project.valid_paths: correct paths"""

    assert projectstarter.valid_paths(*(
        '/home',
        '/home/bar',
        '/home/bar.gif',
        '/var/lib',
    )) == True


def test_wrong_001(projectstarter):
    """project.valid_paths: two identical paths"""

    with pytest.raises(SettingsInvalidError):
        projectstarter.valid_paths(*(
            '/home/foo',
            '/home/bar',
            '/home/foo',
        ))


def test_wrong_002(projectstarter):
    """project.valid_paths: three identical paths"""

    with pytest.raises(SettingsInvalidError):
        projectstarter.valid_paths(*(
            '/home/foo',
            '/home/bar',
            '/home/foo',
            '/home/foo',
        ))


def test_wrong_003(projectstarter):
    """project.valid_paths: multiple identical paths"""

    with pytest.raises(SettingsInvalidError):
        projectstarter.valid_paths(*(
            '/home/foo',
            '/home/bar',
            '/home/foo',
            '/home/bar',
        ))


def test_wrong_004(projectstarter):
    """project.valid_paths: multiple identical paths"""

    with pytest.raises(SettingsInvalidError):
        projectstarter.valid_paths(*(
            '/home/foo',
            '/home/bar',
            '/home/bar',
            '/home/foo',
            '/var/lib',
            '/var/lib',
        ))
