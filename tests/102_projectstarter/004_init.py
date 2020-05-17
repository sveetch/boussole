# -*- coding: utf-8 -*-
import os
import json

import yaml

import pytest

from boussole.exceptions import SettingsInvalidError


@pytest.mark.parametrize("name,ext,module,module_opts", [
    ('json', 'json', json, {}),
    ('yaml', 'yml', yaml, {"Loader": yaml.FullLoader}),
])
def test_success(projectstarter, temp_builds_dir, name, ext, module,
                 module_opts):
    """
    Testing on default values
    """
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

    assert os.path.exists(os.path.join(basedir, settings_filename))
    assert os.path.exists(os.path.join(basedir, "scss"))
    assert os.path.exists(os.path.join(basedir, "css"))

    with open(os.path.join(basedir, settings_filename), "r") as fp:
        assert module.load(fp, **module_opts) == {
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
    """
    Raised exception caused by duplicate paths
    """
    tmp_dirname = 'projectstarter_init_error_{}'.format(name)
    settings_filename = "settings.{}".format(ext)

    basedir = temp_builds_dir.join(tmp_dirname).strpath
    os.makedirs(basedir)

    with pytest.raises(SettingsInvalidError):
        projectstarter(backend_name=name).init(*(
            '.',
            settings_filename,
            'css',
            'css',
        ), cwd=basedir)
