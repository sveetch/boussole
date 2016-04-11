# -*- coding: utf-8 -*-
import os
import pytest


def test_001(settings, finder):
    """finder.ScssFinder: Filter files from partials"""
    sources = [
        '/home/foo/hip.scss',
        '/home/foo/_hop.scss',
        '/home/food/pizza.scss',
        '/home/food/_pasta.scss',
        '/home/food/drink/_azzuro.scss',
    ]

    results = [filepath for filepath in sources \
               if finder.match_conditions(filepath)]


    assert results == [
        '/home/foo/hip.scss',
        '/home/food/pizza.scss',
    ]


def test_002(settings, finder):
    """finder.ScssFinder: Exclude libdirs case 1"""
    sources = [
        '/home/food/pizza.scss',
        '/home/bar/hop.scss',
        '/home/foo/hip.scss',
    ]

    results = []

    for filepath in sources:
        if not finder.match_conditions(filepath,
            sourcedir=None,
            nopartial=False,
            exclude_patterns=[],
            excluded_libdirs=["/home/food", "/home/bar", ]
        ):
            continue

        results.append(filepath)


    assert results == [
        '/home/foo/hip.scss',
    ]


def test_003(settings, finder):
    """finder.ScssFinder: Exclude libdirs case 2"""
    sources = [
        '/home/food/pizza.scss',
        '/home/bar/hop.scss',
        '/home/foo/hip.scss',
    ]

    results = []

    for filepath in sources:
        if not finder.match_conditions(filepath,
            sourcedir=None,
            nopartial=False,
            exclude_patterns=[],
            excluded_libdirs=["/home/foo"]
        ):
            continue

        results.append(filepath)


    assert results == [
        '/home/food/pizza.scss',
        '/home/bar/hop.scss',
    ]


def test_004(settings, finder):
    """finder.ScssFinder: Exclude from patterns but let pass partials"""
    sources = [
        '/home/foo/hip.scss',
        '/home/foo/_hop.scss',
        '/home/food/pizza.scss',
        '/home/food/_pasta.scss',
        '/home/food/drink/_azzuro.scss',
    ]

    results = []

    for filepath in sources:
        if not finder.match_conditions(filepath,
            sourcedir="/home",
            nopartial=False,
            exclude_patterns=[
                "food/*.scss",
            ],
            excluded_libdirs=[]
        ):
            continue

        results.append(filepath)


    assert results == [
        '/home/foo/hip.scss',
        '/home/foo/_hop.scss',
    ]


def test_005(settings, finder):
    """finder.ScssFinder: Filter files from partials and libdirs"""
    sources = [
        '/home/foo/hip.scss',
        '/home/foo/_hop.scss',
        '/home/food/pizza.scss',
        '/home/food/_pasta.scss',
        '/home/food/drink/_azzuro.scss',
        '/etc/sound/bim.scss',
        '/etc/sound/_bam.scss',
        '/etc/sound/boum/kaboom.scss',
    ]

    results = []

    for filepath in sources:
        if not finder.match_conditions(filepath,
            sourcedir="/home/foo",
            exclude_patterns=[],
            excluded_libdirs=["/etc/sound", "/home/food"]
        ):
            continue

        results.append(filepath)


    assert results == [
        '/home/foo/hip.scss',
    ]
