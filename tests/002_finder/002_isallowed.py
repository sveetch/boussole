# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import FinderException

def test_allowed_001(settings, finder):
    """finder.ScssFinder: Allowed simple filename"""
    allowed = finder.is_allowed("foo.scss", excludes=['*.css'])
    assert allowed == True


def test_allowed_002(settings, finder):
    """finder.ScssFinder: Allowed relative filepath"""
    allowed = finder.is_allowed("pika/foo.scss", excludes=['bar/*.scss'])
    assert allowed == True


def test_allowed_003(settings, finder):
    """finder.ScssFinder: Allowed relative filepath"""
    allowed = finder.is_allowed("pika/bar/foo.scss", excludes=['bar/*.scss'])
    assert allowed == True


def test_allowed_004(settings, finder):
    """finder.ScssFinder: Not allowed relative filepath"""
    allowed = finder.is_allowed("pika/bar/foo.scss", excludes=['foo.scss'])
    assert allowed == True


def test_allowed_005(settings, finder):
    """finder.ScssFinder: Allowed relative filepath with many patterns"""
    allowed = finder.is_allowed("pika/bar/foo.scss", excludes=[
        'foo.scss',
        'bar/*.scss',
        '*.css',
    ])
    assert allowed == True


def test_notallowed_100(settings, finder):
    """finder.ScssFinder: Not allowed simple filename"""
    allowed = finder.is_allowed("foo.scss", excludes=['*.scss'])
    assert allowed == False


def test_notallowed_101(settings, finder):
    """finder.ScssFinder: Not allowed simple filename"""
    allowed = finder.is_allowed("foo.scss", excludes=['foo.scss'])
    assert allowed == False


def test_notallowed_102(settings, finder):
    """finder.ScssFinder: Not allowed relative filepath"""
    allowed = finder.is_allowed("pika/foo.scss", excludes=['*.scss'])
    assert allowed == False


def test_notallowed_103(settings, finder):
    """finder.ScssFinder: Not allowed simple filename"""
    allowed = finder.is_allowed("foo.scss", excludes=['*.css', '*.scss'])
    assert allowed == False


def test_notallowed_104(settings, finder):
    """finder.ScssFinder: Not allowed relative filepath"""
    allowed = finder.is_allowed("pika/bar/foo.scss", excludes=['pika/*/*.scss'])
    assert allowed == False


def test_notallowed_105(settings, finder):
    """finder.ScssFinder: Not allowed relative filepath"""
    allowed = finder.is_allowed("pika/bar/plop/foo.scss", excludes=['pika/*/*.scss'])
    assert allowed == False


def test_notallowed_106(settings, finder):
    """finder.ScssFinder: Not allowed relative filepath, matching one of patterns"""
    allowed = finder.is_allowed("pika/bar/foo.scss", excludes=[
        'foo.scss',
        'bar/*.scss',
        'pika/*/*.scss', # bim
        '*.css',
    ])
    assert allowed == False


def test_notallowed_107(settings, finder):
    """finder.ScssFinder: Not allowed relative filepath, matching one of patterns"""
    allowed = finder.is_allowed("pika/bar/foo.scss", excludes=[
        'foo.scss',
        'bar/*.scss',
        '*.scss', # bam
        '*.css',
    ])
    assert allowed == False


def test_allowed_exception_201(settings, finder):
    """finder.ScssFinder: Absolute path raise an exception"""
    with pytest.raises(FinderException):
        allowed = finder.is_allowed("/foo.scss", excludes=[])
