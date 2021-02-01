# -*- coding: utf-8 -*-
import pytest


@pytest.mark.parametrize('path,expected', [
    (
        "",
        False,
    ),
    (
        "foo",
        False,
    ),
    (
        "/home/foo",
        False,
    ),
    (
        "/home/foo/",
        False,
    ),
    (
        "/home/foo.txt",
        False,
    ),
    (
        "/home/foo.scss.part",
        False,
    ),
    (
        "/home/foo.scss.",
        False,
    ),
    (
        "foo.scss",
        True,
    ),
    (
        "/home/foo.css",
        True,
    ),
    (
        "/home/foo.sass",
        True,
    ),
    (
        "/home/foo.scss",
        True,
    ),
])
def test_is_allowed_source(resolver, path, expected):
    assert resolver.is_allowed_source(path) is expected
