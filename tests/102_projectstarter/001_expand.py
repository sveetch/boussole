# -*- coding: utf-8 -*-
import pytest


@pytest.mark.parametrize("sources,expected", [
    # basic
    (
        [
            '.',
            'foo.json',
            'scss',
            'css',
            '/home/foo',
        ],
        (
            '/home/foo',
            '/home/foo/foo.json',
            '/home/foo/scss',
            '/home/foo/css',
        ),
    ),
    # having absolute path for basedir
    (
        [
            '/home/foo',
            'foo.json',
            'scss',
            'css',
            '/home/bar',
        ],
        (
            '/home/foo',
            '/home/foo/foo.json',
            '/home/foo/scss',
            '/home/foo/css',
        ),
    ),
    # absolute basedir but unused because other paths are absolute also
    (
        [
            '/home/bar',
            '/home/foo/foo.json',
            '/home/foo/scss',
            '/home/foo/css',
            '/home/meuh',
        ],
        (
            '/home/bar',
            '/home/foo/foo.json',
            '/home/foo/scss',
            '/home/foo/css',
        ),
    ),
    # using non basic relative paths
    (
        [
            '/home/foo',
            "foo.json",
            "sass/scss",
            "../project/static/css",
            '/home/bar',
        ],
        (
            '/home/foo',
            '/home/foo/foo.json',
            '/home/foo/sass/scss',
            '/home/project/static/css',
        ),
    ),
    # mixin of everything before
    (
        [
            '/home/foo',
            "/home/bar/foo.json",
            "sass/scss",
            "../project/static/css",
            '/home/meuh',
        ],
        (
            '/home/foo',
            '/home/bar/foo.json',
            '/home/foo/sass/scss',
            '/home/project/static/css',
        ),
    ),
])
def test_expand(projectstarter, sources, expected):
    results = projectstarter('json').expand(*sources)

    assert results == expected
