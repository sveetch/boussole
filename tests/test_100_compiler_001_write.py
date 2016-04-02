# -*- coding: utf-8 -*-
import os
import io
import pytest


def test_compiler_write_001(settings, compiler, temp_builds_dir):
    """compiler.SassCompileHelper.write_content: Just creating file with latin
       content"""
    filepath = temp_builds_dir.join('buildhelper_001')

    content = u"""Some sample latin text"""

    compiler.write_content(content, str(filepath))

    # Read file to compare
    with io.open(str(filepath), 'r', encoding='utf-8') as f:
        result = f.read()

    assert content == result


def test_compiler_write_002(settings, compiler, temp_builds_dir):
    """compiler.SassCompileHelper.write_content: Creating file with unicode
       content"""
    filepath = temp_builds_dir.join('buildhelper_002')

    content = u"""Some sample unicode text: フランス Furansu"""

    compiler.write_content(content, str(filepath))

    # Read file to compare
    with io.open(str(filepath), 'r', encoding='utf-8') as f:
        result = f.read()

    assert content == result


def test_compiler_write_003(settings, compiler, temp_builds_dir):
    """compiler.SassCompileHelper.write_content: Creating file into
       subdirectory"""
    filepath = temp_builds_dir.join('foo/bar/home.txt')

    content = u"""Some sample unicode text: フランス Furansu"""

    compiler.write_content(content, str(filepath))

    # Read file to compare
    with io.open(str(filepath), 'r', encoding='utf-8') as f:
        result = f.read()

    assert content == result
