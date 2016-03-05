# -*- coding: utf-8 -*-
import os
import pytest


def test_parser_001_unquote1(settings, parser):
    """parser.ScssImportsParser: unquote case 1"""
    assert parser.strip_quotes("'foo'") == "foo"


def test_parser_001_parse_comment1(settings, parser):
    """parser.ScssImportsParser: commented import 1 (buggy behavior)"""
    result = parser.parse("""//@import "compass/css3";""")
    assert result == []


def test_parser_002_parse_comment2(settings, parser):
    """parser.ScssImportsParser: commented import 2 (buggy behavior)"""
    result = parser.parse("""//      @import "compass/css3";""")
    assert result == []


def test_parser_003_parse_comment3(settings, parser):
    """parser.ScssImportsParser: commented import 3 (buggy behavior)"""
    result = parser.parse("""/*
        @import "compass/css3";
        */""")
    assert result == []

    
def test_parser_100_parse_sample(settings, parser):
    """parser.ScssImportsParser: complete file"""
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


def test_parser_101_parse_empty(settings, parser):
    """parser.ScssImportsParser: empty file"""
    with open(os.path.join(settings.sample_path, '_empty.scss')) as fp:
        result = parser.parse(fp.read())
    assert result == []


def test_parser_102_parse_noimport(settings, parser):
    """parser.ScssImportsParser: no import rules"""
    with open(os.path.join(settings.sample_path, '_vendor.scss')) as fp:
        result = parser.parse(fp.read())
    assert result == []
