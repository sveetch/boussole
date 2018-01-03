# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import FinderException


@pytest.mark.parametrize('filepath,excludes,expected', [
    # Allowed simple filename
    ("foo.scss", ["*.css"], True),
    ("foo.sass", ["*.css"], True),
    # Allowed relative filepath
    ("pika/foo.scss", ["bar/*.scss"], True),
    ("pika/foo.sass", ["bar/*.sass"], True),
    # Allowed relative filepath
    ("pika/bar/foo.scss", ["bar/*.scss"], True),
    ("pika/bar/foo.sass", ["bar/*.sass"], True),
    # Not allowed relative filepath (???)
    ("pika/bar/foo.scss", ["foo.scss"], True),
    ("pika/bar/foo.sass", ["foo.sass"], True),
    # Allowed relative filepath with many patterns
    (
        "pika/bar/foo.scss",
        [
            "foo.scss",
            "bar/*.scss",
            "*.css",
        ],
        True
    ),
    (
        "pika/bar/foo.sass",
        [
            "foo.sass",
            "bar/*.sass",
            "*.css",
        ],
        True
    ),
    # Not allowed simple filename
    ("foo.scss", ["*.scss"], False),
    ("foo.sass", ["*.sass"], False),
    # Not allowed simple filename
    ("foo.scss", ["foo.scss"], False),
    ("foo.sass", ["foo.sass"], False),
    # Not allowed relative filepath
    ("pika/foo.scss", ["*.scss"], False),
    ("pika/foo.sass", ["*.sass"], False),
    # Not allowed simple filename
    ("foo.scss", ['*.css', '*.scss'], False),
    ("foo.sass", ['*.css', '*.sass'], False),
    # Not allowed relative filepath
    ("pika/bar/foo.scss", ['pika/*/*.scss'], False),
    ("pika/bar/foo.sass", ['pika/*/*.sass'], False),
    # Not allowed relative filepath
    ("pika/bar/plop/foo.scss", ['pika/*/*.scss'], False),
    ("pika/bar/plop/foo.sass", ['pika/*/*.sass'], False),
    # Not allowed relative filepath, matching one of patterns
    (
        "pika/bar/foo.scss",
        [
            "foo.scss",
            "bar/*.scss",
            "pika/*/*.scss",
            "*.css",
        ],
        False
    ),
    (
        "pika/bar/foo.sass",
        [
            "foo.sass",
            "bar/*.sass",
            "pika/*/*.sass",
            "*.css",
        ],
        False
    ),
    # Not allowed relative filepath, matching one of patterns
    (
        "pika/bar/foo.scss",
        [
            "foo.scss",
            "bar/*.scss",
            "*.scss",
            "*.css",
        ],
        False
    ),
    (
        "pika/bar/foo.sass",
        [
            "foo.sass",
            "bar/*.sass",
            "*.sass",
            "*.css",
        ],
        False
    ),
])
def test_allowed_001(settings, finder, filepath, excludes, expected):
    """Allowed simple filename"""
    allowed = finder.is_allowed(filepath, excludes=excludes)
    assert expected == allowed


def test_allowed_exception_201(settings, finder):
    """Absolute path raise an exception"""
    with pytest.raises(FinderException):
        allowed = finder.is_allowed("/foo.scss", excludes=[])
