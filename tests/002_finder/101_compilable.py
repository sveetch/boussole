# -*- coding: utf-8 -*-
import os
import pytest


def test_relative_nonrecursive_001(settings, finder):
    """finder.ScssFinder: Find non recursively all compilable sources
       from sample project in relative mode"""
    assert finder.compilable_sources(settings.sample_path, recursive=False) == [
        'main_syntax.scss',
        'main_error.scss',
        'main_circular_5.scss',
        'main_depth_import-2.scss',
        'main_twins_2.scss',
        'main_twins_1.scss',
        'main_circular_0.scss',
        'main_circular_4.scss',
        'main_circular_3.scss',
        'main_twins_3.scss',
        'main_using_libs.scss',
        'main_depth_import-3.scss',
        'main_circular_1.scss',
        'main_depth_import-1.scss',
        'main_commented.scss',
        'main_with_subimports.scss',
        'main_circular_2.scss',
        'main_circular_bridge.scss',
        'main_basic.scss',
    ]


def test_absolute_nonrecursive_002(settings, finder):
    """finder.ScssFinder: Find non recursively all compilable sources
       from sample project in absolute mode"""
    assert finder.compilable_sources(settings.sample_path, absolute=True, recursive=False) == [
        os.path.join(settings.sample_path, 'main_syntax.scss'),
        os.path.join(settings.sample_path, 'main_error.scss'),
        os.path.join(settings.sample_path, 'main_circular_5.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_twins_2.scss'),
        os.path.join(settings.sample_path, 'main_twins_1.scss'),
        os.path.join(settings.sample_path, 'main_circular_0.scss'),
        os.path.join(settings.sample_path, 'main_circular_4.scss'),
        os.path.join(settings.sample_path, 'main_circular_3.scss'),
        os.path.join(settings.sample_path, 'main_twins_3.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_circular_1.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_commented.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_circular_2.scss'),
        os.path.join(settings.sample_path, 'main_circular_bridge.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
    ]


def test_relative_recursive_003(settings, finder):
    """finder.ScssFinder: Find recursively all compilable sources from
       sample project in relative mode"""
    assert finder.compilable_sources(settings.sample_path) == [
        'main_syntax.scss',
        'main_error.scss',
        'main_circular_5.scss',
        'main_depth_import-2.scss',
        'main_twins_2.scss',
        'main_twins_1.scss',
        'main_circular_0.scss',
        'main_circular_4.scss',
        'main_circular_3.scss',
        'main_twins_3.scss',
        'main_using_libs.scss',
        'main_depth_import-3.scss',
        'main_circular_1.scss',
        'main_depth_import-1.scss',
        'main_commented.scss',
        'main_with_subimports.scss',
        'main_circular_2.scss',
        'main_circular_bridge.scss',
        'main_basic.scss',
        'components/twin_3.scss',
        'components/twin_2.scss',
    ]


def test_absolute_recursive_004(settings, finder):
    """finder.ScssFinder: Find recursively all compilable sources from
       sample project in absolute mode"""
    assert finder.compilable_sources(settings.sample_path, absolute=True) == [
        os.path.join(settings.sample_path, 'main_syntax.scss'),
        os.path.join(settings.sample_path, 'main_error.scss'),
        os.path.join(settings.sample_path, 'main_circular_5.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_twins_2.scss'),
        os.path.join(settings.sample_path, 'main_twins_1.scss'),
        os.path.join(settings.sample_path, 'main_circular_0.scss'),
        os.path.join(settings.sample_path, 'main_circular_4.scss'),
        os.path.join(settings.sample_path, 'main_circular_3.scss'),
        os.path.join(settings.sample_path, 'main_twins_3.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_circular_1.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_commented.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_circular_2.scss'),
        os.path.join(settings.sample_path, 'main_circular_bridge.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'components/twin_3.scss'),
        os.path.join(settings.sample_path, 'components/twin_2.scss'),
    ]


def test_relative_subdir_005(settings, finder):
    """finder.ScssFinder: Find recursively all compilable sources from
       sample project subdirectory in relative mode"""
    assert finder.compilable_sources(os.path.join(settings.sample_path, 'components')) == [
        'twin_3.scss',
        'twin_2.scss',
    ]


def test_absolute_subdir_006(settings, finder):
    """finder.ScssFinder: Find recursively all compilable sources from
       sample project subdirectory in absolute mode"""
    assert finder.compilable_sources(os.path.join(settings.sample_path, 'components'), absolute=True) == [
        os.path.join(settings.sample_path, 'components/twin_3.scss'),
        os.path.join(settings.sample_path, 'components/twin_2.scss'),
    ]


def test_relative_exclude_007(settings, finder):
    """finder.ScssFinder: Find recursively all compilable sources with
       excluding patterns on relative mode"""
    excludes = [
        'main_error.scss',
        'main_circular_5.scss',
        'main_circular_0.scss',
        'main_circular_4.scss',
        'main_circular_3.scss',
        'main_circular_1.scss',
        'main_circular_2.scss',
        'main_circular_bridge.scss',
        '*/twin_3.scss',
    ]

    assert finder.compilable_sources(settings.sample_path, excludes=excludes) == [
        'main_syntax.scss',
        'main_depth_import-2.scss',
        'main_twins_2.scss',
        'main_twins_1.scss',
        'main_twins_3.scss',
        'main_using_libs.scss',
        'main_depth_import-3.scss',
        'main_depth_import-1.scss',
        'main_commented.scss',
        'main_with_subimports.scss',
        'main_basic.scss',
        'components/twin_2.scss',
    ]


def test_absolute_exclude_008(settings, finder):
    """finder.ScssFinder: Find recursively all compilable sources with
       excluding patterns on absolute mode"""
    excludes = [
        'main_error.scss',
        'main_circular_5.scss',
        'main_circular_0.scss',
        'main_circular_4.scss',
        'main_circular_3.scss',
        'main_circular_1.scss',
        'main_circular_2.scss',
        'main_circular_bridge.scss',
        '*/twin_3.scss',
    ]

    assert finder.compilable_sources(settings.sample_path, absolute=True, excludes=excludes) == [
        os.path.join(settings.sample_path, 'main_syntax.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_twins_2.scss'),
        os.path.join(settings.sample_path, 'main_twins_1.scss'),
        os.path.join(settings.sample_path, 'main_twins_3.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_commented.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'components/twin_2.scss'),
    ]
