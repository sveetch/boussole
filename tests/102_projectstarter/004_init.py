# -*- coding: utf-8 -*-
import os
import json
import pytest

from boussole.exceptions import SettingsInvalidError


def test_success_001(projectstarter, temp_builds_dir):
    """project.init: Testing on default values"""
    basedir = temp_builds_dir.join('projectstarter_init_success_001').strpath
    os.makedirs(basedir)

    results = projectstarter.init(*(
        '.',
        'settings.json',
        'scss',
        'css',
    ), cwd=basedir)

    assert results == {
        "basedir": basedir,
        "config": os.path.join(basedir, "settings.json"),
        "sourcedir": os.path.join(basedir, "scss"),
        "targetdir": os.path.join(basedir, "css"),
    }

    assert os.path.exists(os.path.join(basedir, "settings.json")) == True
    assert os.path.exists(os.path.join(basedir, "scss")) == True
    assert os.path.exists(os.path.join(basedir, "css")) == True

    with open(os.path.join(basedir, "settings.json"), "rb") as fp:
        assert json.load(fp) == {
            'SOURCES_PATH': 'scss',
            'TARGET_PATH': 'css',
            "LIBRARY_PATHS": [],
            "OUTPUT_STYLES": "nested",
            "SOURCE_COMMENTS": False,
            "EXCLUDES": []
        }


def test_error_001(projectstarter, temp_builds_dir):
    """project.init: Raised exception caused by duplicate paths"""
    basedir = temp_builds_dir.join('projectstarter_init_error_001').strpath
    os.makedirs(basedir)

    with pytest.raises(SettingsInvalidError):
        results = projectstarter.init(*(
            '.',
            'settings.json',
            'css',
            'css',
        ), cwd=basedir)
