# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.patcher import SettingsPatcher


def test_conf_patcher_001_expand_nothingtodo(settings,
                                             sample_project_settings):
    """conf.patcher.SettingsPatcher: Nothing to expand, path is correct"""
    patcher = SettingsPatcher()

    expand_result = patcher._patch_expand_path(sample_project_settings, "DUMMY_NAME", "/foo/bar")

    assert expand_result == "/foo/bar"


def test_conf_patcher_002_expand_homedir(settings,
                                             sample_project_settings):
    """conf.patcher.SettingsPatcher: Single path expand home user dir"""
    patcher = SettingsPatcher()

    expand_result = patcher._patch_expand_path(sample_project_settings, "DUMMY_NAME", "~/foo")

    assert expand_result == os.path.join(os.environ['HOME'], 'foo')


def test_conf_patcher_003_expand_absolute(settings,
                                             sample_project_settings):
    """conf.patcher.SettingsPatcher: Single path expand to absolute dir"""
    patcher = SettingsPatcher()
    patcher.projectdir = settings.fixtures_path

    expand_result = patcher._patch_expand_path(sample_project_settings,
                                               "DUMMY_NAME",
                                               "tests/data_fixtures/sample_project")

    assert expand_result == os.path.join(settings.fixtures_path,
                                         "tests/data_fixtures/sample_project")


def test_conf_patcher_004_expand_wrong(settings,
                                             sample_project_settings):
    """conf.patcher.SettingsPatcher: The path does not exists but is expanded
       to absolute from current dir"""
    patcher = SettingsPatcher()
    patcher.projectdir = "/home/user"

    expand_result = patcher._patch_expand_path(sample_project_settings,
                                               "DUMMY_NAME", "foo/coco/bar")

    assert expand_result == os.path.join("/home/user", "foo/coco/bar")


def test_conf_patcher_005_expand_normpath(settings,
                                             sample_project_settings):
    """conf.patcher.SettingsPatcher: Single path expand to absolute dir
       normalized"""
    patcher = SettingsPatcher()
    patcher.projectdir = settings.fixtures_path

    expand_result = patcher._patch_expand_path(sample_project_settings,
                                               "DUMMY_NAME",
                                               "tests/data_fixtures/foo/../sample_project")

    assert expand_result == os.path.join(settings.fixtures_path,
                                         "tests/data_fixtures/sample_project")


def test_conf_patcher_010_expands(settings, sample_project_settings):
    """conf.patcher.SettingsPatcher: Expand a list of path"""
    patcher = SettingsPatcher()
    patcher.projectdir = settings.fixtures_path

    current_dir = os.getcwd()

    paths = [
        "/foo/bar",
        "~/foo",
        "tests/data_fixtures/sample_project",
        "tests/data_fixtures/foo/../sample_project",
        "foo/coco/bar",
    ]

    expected = [
        "/foo/bar",
        os.path.join(os.environ['HOME'], 'foo'),
        os.path.join(settings.fixtures_path, "tests/data_fixtures/sample_project"),
        os.path.join(settings.fixtures_path, "tests/data_fixtures/sample_project"),
        os.path.join(settings.fixtures_path, "foo/coco/bar"),
    ]

    expand_result = patcher._patch_expand_paths(sample_project_settings, "DUMMY_NAME", paths)

    assert expand_result == expected
