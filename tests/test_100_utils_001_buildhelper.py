# -*- coding: utf-8 -*-
import os
import io
import pytest

from boussole.utils import build_target_helper


def test_utils_buildhelper_001(settings, temp_builds_dir):
    """utils.build_target_helper: Just creating file with latin content"""
    filepath = temp_builds_dir.join('buildhelper_001')

    content = u"""Some sample latin text"""

    build_target_helper(content, str(filepath))

    # Read file to compare
    with io.open(str(filepath), 'r', encoding='utf-8') as f:
        result = f.read()

    assert content == result


def test_utils_buildhelper_002(settings, temp_builds_dir):
    """utils.build_target_helper: Creating file with unicode content"""
    filepath = temp_builds_dir.join('buildhelper_002')

    content = u"""Some sample unicode text: フランス Furansu"""

    build_target_helper(content, str(filepath))

    # Read file to compare
    with io.open(str(filepath), 'r', encoding='utf-8') as f:
        result = f.read()

    assert content == result


def test_utils_buildhelper_003(settings, temp_builds_dir):
    """utils.build_target_helper: Creating file into subdirectory"""
    filepath = temp_builds_dir.join('foo/bar/home.txt')

    content = u"""Some sample unicode text: フランス Furansu"""

    build_target_helper(content, str(filepath))

    # Read file to compare
    with io.open(str(filepath), 'r', encoding='utf-8') as f:
        result = f.read()

    assert content == result
