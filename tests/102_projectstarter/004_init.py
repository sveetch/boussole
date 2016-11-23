# -*- coding: utf-8 -*-
import os
import json
import yaml

import pytest

from boussole.exceptions import SettingsInvalidError


@pytest.mark.parametrize("name,ext,module", [
    ('json', 'json', json),
    ('yaml', 'yml', yaml),
])
def test_success(projectstarter, temp_builds_dir, name, ext, module):
    """Testing on default values"""
    tmp_dirname = 'projectstarter_init_success_{}'.format(name)
    settings_filename = "settings.{}".format(ext)

    basedir = temp_builds_dir.join(tmp_dirname).strpath
    os.makedirs(basedir)

    results = projectstarter(backend_name=name).init(*(
        '.',
        settings_filename,
        'scss',
        'css',
    ), cwd=basedir)

    assert results == {
        "basedir": basedir,
        "config": os.path.join(basedir, settings_filename),
        "sourcedir": os.path.join(basedir, "scss"),
        "targetdir": os.path.join(basedir, "css"),
    }

    assert os.path.exists(os.path.join(basedir, settings_filename)) == True
    assert os.path.exists(os.path.join(basedir, "scss")) == True
    assert os.path.exists(os.path.join(basedir, "css")) == True

    with open(os.path.join(basedir, settings_filename), "r") as fp:
        assert module.load(fp) == {
            'SOURCES_PATH': 'scss',
            'TARGET_PATH': 'css',
            "LIBRARY_PATHS": [],
            "OUTPUT_STYLES": "nested",
            "SOURCE_COMMENTS": False,
            "EXCLUDES": []
        }


@pytest.mark.parametrize("name,ext,module", [
    ('json', 'json', json),
    ('yaml', 'yml', yaml),
])
def test_error(projectstarter, temp_builds_dir, name, ext, module):
    """Raised exception caused by duplicate paths"""
    tmp_dirname = 'projectstarter_init_error_{}'.format(name)
    settings_filename = "settings.{}".format(ext)

    basedir = temp_builds_dir.join(tmp_dirname).strpath
    os.makedirs(basedir)

    with pytest.raises(SettingsInvalidError):
        results = projectstarter(backend_name=name).init(*(
            '.',
            settings_filename,
            'css',
            'css',
        ), cwd=basedir)

