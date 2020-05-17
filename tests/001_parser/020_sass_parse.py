# -*- coding: utf-8 -*-
"""
Sass indented syntax tests only cover differences with scss syntax
"""
import os


def test_sample_001(settings, sass_parser):
    """Complete file"""
    with open(os.path.join(settings.sass_sample_path, 'main_syntax.sass')) as fp:
        result = sass_parser.parse(fp.read())
    assert result == [
        'vendor', 'utils/mixins', 'sass_filetest', 'css_filetest', '_empty',
        'components/filename_test_1', 'components/_filename_test_2',
        'components/filename_test_3.scss',
        'components/_filename_test_4.scss',
        'components/filename_test_5.plop',
        'components/filename_test_6.plop.scss',
        'components/../empty',
    ]


def test_newline_001(settings, sass_parser):
    """
    Imports with ending newline is always parsed right
    """
    content = (
        """// Foo\n"""
        """@import candidate1\n"""
        """@import candidate2\n"""
    )
    result = sass_parser.parse(content)
    assert result == ["candidate1", "candidate2"]


def test_newline_002(settings, sass_parser):
    """
    Ensure nothing after import newline is wrongly captured
    """
    content = (
        """// Foo\n"""
        """@import candidate1\n"""
        """@import candidate2\n"""
        """.foo{ color: red }"""
    )
    result = sass_parser.parse(content)
    assert result == ["candidate1", "candidate2"]


def test_newline_003(settings, sass_parser):
    """
    Import with no newline when it is placed at the end of file should be
    parsed right also
    """
    content = (
        """// Foo\n"""
        """@import candidate1\n"""
        """@import candidate2"""
    )
    result = sass_parser.parse(content)
    assert result == ["candidate1", "candidate2"]


def test_empty_001(settings, sass_parser):
    """empty file"""
    with open(os.path.join(settings.sass_sample_path, '_empty.sass')) as fp:
        result = sass_parser.parse(fp.read())
    assert result == []


def test_noimport_001(settings, sass_parser):
    """no import rules"""
    with open(os.path.join(settings.sass_sample_path, '_vendor.sass')) as fp:
        result = sass_parser.parse(fp.read())
    assert result == []
