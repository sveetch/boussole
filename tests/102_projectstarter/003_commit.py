# -*- coding: utf-8 -*-
import os
import json
import yaml
import pytest

@pytest.mark.parametrize("name,ext,module", [
    ('json', 'json', json),
    ('yaml', 'yml', yaml),
])
def test_commit_basic(projectstarter, temp_builds_dir, name, ext, module):
    """Commit with basic values for every backends"""
    tmp_dirname = 'projectstarter_commit_{}'.format(name)
    settings_filename = "settings.{}".format(ext)

    basedir = temp_builds_dir.join(tmp_dirname).strpath
    os.makedirs(basedir)

    opts = (
        "scss",
        "css",
        os.path.join(basedir, settings_filename),
        os.path.join(basedir, "scss"),
        os.path.join(basedir, "css"),
    )

    projectstarter().commit(*opts)

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
