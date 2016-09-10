# -*- coding: utf-8 -*-
import os
import pytest


def test_comment_001(settings, parser):
    """commented import 1 (buggy behavior)"""
    result = parser.parse("""//@import "compass/css3";""")
    assert result == []


def test_comment_002(settings, parser):
    """commented import 2 (buggy behavior)"""
    result = parser.parse("""//      @import "compass/css3";""")
    assert result == []


def test_comment_003(settings, parser):
    """commented import 3 (buggy behavior)"""
    result = parser.parse("""/*
        @import "compass/css3";
        */""")
    assert result == []


def test_unicode(settings, parser):
    """Just checkin parser on unicode character"""
    result = parser.parse(u"""// Look this unicode char: →""")
    assert result == []


def test_sample_001(settings, parser):
    """Complete file"""
    with open(os.path.join(settings.sample_path, 'main_syntax.scss')) as fp:
        result = parser.parse(fp.read())
    assert result == [
        'vendor', 'utils/mixins', 'sass_filetest', 'css_filetest', '_empty',
        'components/filename_test_1', 'components/_filename_test_2',
        'components/filename_test_3.scss',
        'components/_filename_test_4.scss',
        'components/filename_test_5.plop',
        'components/filename_test_6.plop.scss',
        'components/../empty',
    ]


def test_empty_001(settings, parser):
    """empty file"""
    with open(os.path.join(settings.sample_path, '_empty.scss')) as fp:
        result = parser.parse(fp.read())
    assert result == []


def test_noimport_001(settings, parser):
    """no import rules"""
    with open(os.path.join(settings.sample_path, '_vendor.scss')) as fp:
        result = parser.parse(fp.read())
    assert result == []
