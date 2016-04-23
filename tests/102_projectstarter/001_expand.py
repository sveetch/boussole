# -*- coding: utf-8 -*-
import os
import json
import pytest


def test_001(projectstarter):
    """project.expand: basic"""

    results = projectstarter.expand(*[
        '.',
        'settings.json',
        'scss',
        'css',
        '/home/foo',
    ])

    assert results == (
        '/home/foo',
        '/home/foo/settings.json',
        '/home/foo/scss',
        '/home/foo/css',
    )


def test_002(projectstarter):
    """project.expand: having absolute path for basedir"""

    results = projectstarter.expand(*[
        '/home/foo',
        'settings.json',
        'scss',
        'css',
        '/home/bar',
    ])

    assert results == (
        '/home/foo',
        '/home/foo/settings.json',
        '/home/foo/scss',
        '/home/foo/css',
    )


def test_003(projectstarter):
    """project.expand: absolute basedir but unused because other paths are absolute also"""

    results = projectstarter.expand(*[
        '/home/bar',
        '/home/foo/settings.json',
        '/home/foo/scss',
        '/home/foo/css',
        '/home/meuh',
    ])

    assert results == (
        '/home/bar',
        '/home/foo/settings.json',
        '/home/foo/scss',
        '/home/foo/css',
    )


def test_004(projectstarter):
    """project.expand: using non basic relative paths"""

    results = projectstarter.expand(*[
        '/home/foo',
        "settings.json",
        "sass/scss",
        "../project/static/css",
        '/home/bar',
    ])

    assert results == (
        '/home/foo',
        '/home/foo/settings.json',
        '/home/foo/sass/scss',
        '/home/project/static/css',
    )


def test_004(projectstarter):
    """project.expand: mixin of everything before"""

    results = projectstarter.expand(*[
        '/home/foo',
        "/home/bar/settings.json",
        "sass/scss",
        "../project/static/css",
        '/home/meuh',
    ])

    assert results == (
        '/home/foo',
        '/home/bar/settings.json',
        '/home/foo/sass/scss',
        '/home/project/static/css',
    )
