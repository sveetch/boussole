# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.exceptions import SettingsInvalidError
from boussole.conf.post_processor import SettingsPostProcessor


def test_001_success(settings):
    """conf.post_processor.SettingsPostProcessor: Validate required value on dummy value"""
    processor = SettingsPostProcessor()

    result = processor._validate_required({}, "DUMMY_NAME", "foo")
    assert result == "foo"


def test_002_fail(settings):
    """conf.post_processor.SettingsPostProcessor: Validate existing file on empty value"""
    processor = SettingsPostProcessor()

    with pytest.raises(SettingsInvalidError):
        processor._validate_required({}, "DUMMY_NAME", "")


def test_003_fail(settings):
    """conf.post_processor.SettingsPostProcessor: Validate existing file on empty value"""
    processor = SettingsPostProcessor()

    with pytest.raises(SettingsInvalidError):
        processor._validate_required({}, "DUMMY_NAME", None)
