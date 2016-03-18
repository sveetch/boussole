# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf import Settings


def test_conf_settings_patch_001_expand_clean(settings, 
                                             sample_project_settings):
    """conf.Settings: Nothing to expand, path is correct"""
    settings_object = Settings()
    
    expand_result = settings_object._patch_expand_path(sample_project_settings, "dummy", "/foo/bar")
    
    assert expand_result == "/foo/bar"


def test_conf_settings_patch_002_expand_homedir(settings, 
                                             sample_project_settings):
    """conf.Settings: Single path expand home user dir"""
    settings_object = Settings()
    
    expand_result = settings_object._patch_expand_path(sample_project_settings, "dummy", "~/foo")
    
    assert expand_result == os.path.join(os.environ['HOME'], 'foo')


def test_conf_settings_patch_003_expand_absolute(settings, 
                                             sample_project_settings):
    """conf.Settings: Single path expand to absolute dir"""
    settings_object = Settings()
    
    current_dir = os.getcwd()
    
    expand_result = settings_object._patch_expand_path(sample_project_settings, "dummy", "tests/data_fixtures/sample_project")
    
    assert expand_result == os.path.join(current_dir, "tests/data_fixtures/sample_project")


def test_conf_settings_patch_004_expand_wrong(settings, 
                                             sample_project_settings):
    """conf.Settings: The path does not exists but is expanded to absolute
       from current dir"""
    settings_object = Settings()
    
    current_dir = os.getcwd()
    
    expand_result = settings_object._patch_expand_path(sample_project_settings, "dummy", "foo/coco/bar")
    
    assert expand_result == os.path.join(current_dir, "foo/coco/bar")


def test_conf_settings_patch_010_expands(settings, 
                                             sample_project_settings):
    """conf.Settings: Expand a list of path"""
    settings_object = Settings()
    
    current_dir = os.getcwd()
    
    paths = [
        "/foo/bar",
        "~/foo",
        "tests/data_fixtures/sample_project",
        "foo/coco/bar",
    ]
    
    expected = [
        "/foo/bar",
        os.path.join(os.environ['HOME'], 'foo'),
        os.path.join(current_dir, "tests/data_fixtures/sample_project"),
        os.path.join(current_dir, "foo/coco/bar"),
    ]
    
    expand_result = settings_object._patch_expand_paths(sample_project_settings, "dummy", paths)
    
    assert expand_result == expected
