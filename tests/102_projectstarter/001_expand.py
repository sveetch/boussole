# -*- coding: utf-8 -*-
import os
import json
import pytest


@pytest.mark.parametrize("sources,attempted", [
    # basic
    (
        [
            '.',
            'settings.json',
            'scss',
            'css',
            '/home/foo',
        ],
        (
            '/home/foo',
            '/home/foo/settings.json',
            '/home/foo/scss',
            '/home/foo/css',
        ),
    ),
    # having absolute path for basedir
    (
        [
            '/home/foo',
            'settings.json',
            'scss',
            'css',
            '/home/bar',
        ],
        (
            '/home/foo',
            '/home/foo/settings.json',
            '/home/foo/scss',
            '/home/foo/css',
        ),
    ),
    # absolute basedir but unused because other paths are absolute also
    (
        [
            '/home/bar',
            '/home/foo/settings.json',
            '/home/foo/scss',
            '/home/foo/css',
            '/home/meuh',
        ],
        (
            '/home/bar',
            '/home/foo/settings.json',
            '/home/foo/scss',
            '/home/foo/css',
        ),
    ),
    # using non basic relative paths
    (
        [
            '/home/foo',
            "settings.json",
            "sass/scss",
            "../project/static/css",
            '/home/bar',
        ],
        (
            '/home/foo',
            '/home/foo/settings.json',
            '/home/foo/sass/scss',
            '/home/project/static/css',
        ),
    ),
    # mixin of everything before
    (
        [
            '/home/foo',
            "/home/bar/settings.json",
            "sass/scss",
            "../project/static/css",
            '/home/meuh',
        ],
        (
            '/home/foo',
            '/home/bar/settings.json',
            '/home/foo/sass/scss',
            '/home/project/static/css',
        ),
    ),
])
def test_expand(projectstarter, sources, attempted):
    results = projectstarter().expand(*sources)

    assert results == attempted
