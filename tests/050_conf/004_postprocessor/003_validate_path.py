# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.exceptions import SettingsInvalidError
from boussole.conf.post_processor import SettingsPostProcessor


def test_001_success(settings, temp_builds_dir):
    """conf.post_processor.SettingsPostProcessor: Validate existing file path"""
    basedir = temp_builds_dir.join('postprocessor_validate_path_001')
    os.makedirs(basedir.strpath)

    processor = SettingsPostProcessor()

    foo = basedir.join('foo.txt')
    foo.write("Hello world!")

    result = processor._validate_path({}, "DUMMY_NAME", foo.strpath)

    assert result == foo.strpath


def test_002_exception(settings, temp_builds_dir):
    """conf.post_processor.SettingsPostProcessor: Validate not existing file path"""
    basedir = temp_builds_dir.join('postprocessor_validate_path_002')
    os.makedirs(basedir.strpath)

    processor = SettingsPostProcessor()

    foo = basedir.join('foo.txt')

    with pytest.raises(SettingsInvalidError):
        result = processor._validate_path({}, "DUMMY_NAME", foo.strpath)


def test_003_list_success(settings, temp_builds_dir):
    """conf.post_processor.SettingsPostProcessor: Validate existing file paths"""
    basedir = temp_builds_dir.join('postprocessor_validate_path_003')
    os.makedirs(basedir.strpath)

    processor = SettingsPostProcessor()

    foo = basedir.join('foo.txt')
    foo.write("Hello world!")

    bar = basedir.join('bar.txt')
    bar.write("Hello plop!")

    result = processor._validate_paths({}, "DUMMY_NAME", (
        foo.strpath,
        bar.strpath,
    ))

    assert result == [
        foo.strpath,
        bar.strpath,
    ]


def test_004_list_exception(settings, temp_builds_dir):
    """conf.post_processor.SettingsPostProcessor: Validate existing file paths"""
    basedir = temp_builds_dir.join('postprocessor_validate_path_004')
    os.makedirs(basedir.strpath)

    processor = SettingsPostProcessor()

    foo = basedir.join('foo.txt')
    foo.write("Hello world!")

    bar = basedir.join('bar.txt')
    bar.write("Hello plop!")

    with pytest.raises(SettingsInvalidError):
        result = processor._validate_paths({}, "DUMMY_NAME", (
            foo.strpath,
            "meh",
            bar.strpath,
        ))
