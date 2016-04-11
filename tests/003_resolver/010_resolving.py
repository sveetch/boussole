# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import UnresolvablePath
from boussole.exceptions import UnclearResolution

def test_basic(settings, parser, resolver):
    """resolver.ImportPathsResolver: Resolve paths from basic sample"""
    sourcepath = os.path.join(settings.sample_path, 'main_basic.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())

    resolved_paths = resolver.resolve(sourcepath, finded_paths)

    assert resolved_paths == [
        os.path.join(settings.sample_path, '_vendor.scss'),
        os.path.join(settings.sample_path, '_empty.scss'),
    ]


def test_library(settings, parser, resolver):
    """resolver.ImportPathsResolver: Resolve paths from main_using_libs.scss
    that use included libraries"""
    sourcepath = os.path.join(settings.sample_path, 'main_using_libs.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())

    resolved_paths = resolver.resolve(
        sourcepath,
        finded_paths,
        library_paths=settings.libraries_fixture_paths
    )

    assert resolved_paths == [
        os.path.join(settings.lib2_path, 'addons/_some_addon.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'components/_webfont.scss'),
        os.path.join(settings.lib1_path, 'library_1_fullstack.scss'),
    ]


def test_commented(settings, parser, resolver):
    """resolver.ImportPathsResolver: Resolve paths from sample with comments"""
    sourcepath = os.path.join(settings.sample_path, 'main_commented.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())

    resolved_paths = resolver.resolve(sourcepath, finded_paths)

    assert resolved_paths == [
        os.path.join(settings.sample_path, '_vendor.scss'),
        os.path.join(settings.sample_path, 'components/_filename_test_1.scss'),
        os.path.join(settings.sample_path, '_empty.scss'),
        os.path.join(settings.sample_path, 'components/_webfont.scss'),
        os.path.join(settings.sample_path, 'components/_filename_test_2.scss'),
    ]


def test_error_unresolvable(settings, parser, resolver):
    """resolver.ImportPathsResolver: Exception on wrong import path"""
    sourcepath = os.path.join(settings.sample_path, 'main_error.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())

    with pytest.raises(UnresolvablePath):
        resolver.resolve(
            sourcepath,
            finded_paths,
            library_paths=settings.libraries_fixture_paths
        )


def test_error_unclear_001(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates on unclear resolution"""
    sourcepath = os.path.join(settings.sample_path, 'main_twins_1.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())

    with pytest.raises(UnclearResolution):
        resolver.resolve(
            sourcepath,
            finded_paths,
            library_paths=settings.libraries_fixture_paths
        )


def test_error_unclear_002(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates on unclear resolution"""
    sourcepath = os.path.join(settings.sample_path, 'main_twins_2.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())

    with pytest.raises(UnclearResolution):
        resolver.resolve(
            sourcepath,
            finded_paths,
            library_paths=settings.libraries_fixture_paths
        )


def test_error_unclear_003(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates on explicit resolution"""
    sourcepath = os.path.join(settings.sample_path, 'main_twins_3.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())

    results = resolver.resolve(
        sourcepath,
        finded_paths,
        library_paths=settings.libraries_fixture_paths
    )

    assert results == [
        os.path.join(settings.sample_path, '_vendor.scss'),
        os.path.join(settings.sample_path, 'components/_twin_3.scss'),
    ]
