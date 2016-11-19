# -*- coding: utf-8 -*-
import os
import json
import yaml
import pytest


def test_json(projectstarter, temp_builds_dir):
    """project.init_project: Testing on basic values"""
    basedir = temp_builds_dir.join('projectstarter_commit_json').strpath
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

    with open(os.path.join(basedir, "settings.json"), "r") as fp:
        assert json.load(fp) == {
            'SOURCES_PATH': 'scss',
            'TARGET_PATH': 'css',
            "LIBRARY_PATHS": [],
            "OUTPUT_STYLES": "nested",
            "SOURCE_COMMENTS": False,
            "EXCLUDES": []
        }


def test_yaml(projectstarter, temp_builds_dir):
    """project.init_project: Testing on basic values"""
    basedir = temp_builds_dir.join('projectstarter_commit_yaml').strpath
    os.makedirs(basedir)

    opts = (
        "scss",
        "css",
        os.path.join(basedir, "settings.yml"),
        os.path.join(basedir, "scss"),
        os.path.join(basedir, "css"),
    )

    projectstarter.commit(*opts)

    assert os.path.exists(os.path.join(basedir, "settings.yml")) == True
    assert os.path.exists(os.path.join(basedir, "scss")) == True
    assert os.path.exists(os.path.join(basedir, "css")) == True

    with open(os.path.join(basedir, "settings.yml"), "r") as fp:
        assert yaml.load(fp) == {
            'SOURCES_PATH': 'scss',
            'TARGET_PATH': 'css',
            "LIBRARY_PATHS": [],
            "OUTPUT_STYLES": "nested",
            "SOURCE_COMMENTS": False,
            "EXCLUDES": []
        }
