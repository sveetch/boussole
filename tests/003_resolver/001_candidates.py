# -*- coding: utf-8 -*-
import pytest


def test_basic(settings, parser, resolver):
    """resolver.ImportPathsResolver: Underscore leading and candidate extensions"""
    assert resolver.candidate_paths("foo") == [
        "foo.scss",
        "_foo.scss",
        "foo.sass",
        "_foo.sass",
        "foo.css",
        "_foo.css",
    ]


def test_extension_uncandidate(settings, parser, resolver):
    """resolver.ImportPathsResolver: Uncandidate extension"""
    assert resolver.candidate_paths("foo.plop") == [
        "foo.plop.scss",
        "_foo.plop.scss",
        "foo.plop.sass",
        "_foo.plop.sass",
        "foo.plop.css",
        "_foo.plop.css",
    ]


def test_extension_ready(settings, parser, resolver):
    """resolver.ImportPathsResolver: Candidate extension allready in place"""
    assert resolver.candidate_paths("foo.scss") == [
        "foo.scss",
        "_foo.scss",
    ]


def test_complex_001(settings, parser, resolver):
    """resolver.ImportPathsResolver: Complex case 1 for candidates"""
    assert resolver.candidate_paths("components/addons/foo.plop.scss") == [
        "components/addons/foo.plop.scss",
        "components/addons/_foo.plop.scss",
    ]


def test_complex_002(settings, parser, resolver):
    """resolver.ImportPathsResolver: Complex case 2 for candidates"""
    assert resolver.candidate_paths("../components/../addons/foo.plop") == [
        "../components/../addons/foo.plop.scss",
        "../components/../addons/_foo.plop.scss",
        "../components/../addons/foo.plop.sass",
        "../components/../addons/_foo.plop.sass",
        "../components/../addons/foo.plop.css",
        "../components/../addons/_foo.plop.css",
    ]
