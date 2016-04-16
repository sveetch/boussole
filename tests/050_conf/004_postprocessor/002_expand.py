# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.post_processor import SettingsPostProcessor


def test_001_expand_nothingtodo(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Nothing to expand, path is correct"""
    processor = SettingsPostProcessor()

    expand_result = processor._patch_expand_path(sample_project_settings, "DUMMY_NAME", "/foo/bar")

    assert expand_result == "/foo/bar"


def test_002_expand_homedir(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Single path expand home user dir"""
    processor = SettingsPostProcessor()

    expand_result = processor._patch_expand_path(sample_project_settings, "DUMMY_NAME", "~/foo")

    assert expand_result == os.path.join(os.environ['HOME'], 'foo')


def test_003_expand_absolute(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Single path expand to absolute dir"""
    processor = SettingsPostProcessor()
    processor.projectdir = settings.fixtures_path

    expand_result = processor._patch_expand_path(sample_project_settings,
                                               "DUMMY_NAME",
                                               "tests/data_fixtures/sample_project")

    assert expand_result == os.path.join(settings.fixtures_path,
                                         "tests/data_fixtures/sample_project")


def test_004_expand_wrong(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: The path does not exists but is expanded
       to absolute from current dir"""
    processor = SettingsPostProcessor()
    processor.projectdir = "/home/user"

    expand_result = processor._patch_expand_path(sample_project_settings,
                                               "DUMMY_NAME", "foo/coco/bar")

    assert expand_result == os.path.join("/home/user", "foo/coco/bar")


def test_005_expand_normpath(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Single path expand to absolute dir
       normalized"""
    processor = SettingsPostProcessor()
    processor.projectdir = settings.fixtures_path

    expand_result = processor._patch_expand_path(sample_project_settings,
                                               "DUMMY_NAME",
                                               "tests/data_fixtures/foo/../sample_project")

    assert expand_result == os.path.join(settings.fixtures_path,
                                         "tests/data_fixtures/sample_project")


def test_010_expands(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Expand a list of path"""
    processor = SettingsPostProcessor()
    processor.projectdir = settings.fixtures_path

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

    expand_result = processor._patch_expand_paths(sample_project_settings, "DUMMY_NAME", paths)

    assert expand_result == expected
