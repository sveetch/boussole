# -*- coding: utf-8 -*-
import os
import json
import pytest


def test_001(projectstarter, temp_builds_dir):
    """project.init_project: Testing on basic values"""
    basedir = temp_builds_dir.join('projectstarter_commit_001').strpath
    os.makedirs(basedir)

    opts = (
        "scss",
        "css",
        os.path.join(basedir, "settings.json"),
        os.path.join(basedir, "scss"),
        os.path.join(basedir, "css"),
    )

    projectstarter.commit(*opts)

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
