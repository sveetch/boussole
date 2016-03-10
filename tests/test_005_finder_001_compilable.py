# -*- coding: utf-8 -*-
import os
import pytest

def test_finder_compilable_001(settings, finder):
    """finder.ScssInspector: Find non recursively all compilable sources
       from sample project"""
    assert finder.get_compilable_sources([settings.sample_path], recursive=False) == [
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

def test_finder_compilable_002(settings, finder):
    """finder.ScssInspector: Find recursively all compilable sources from
       sample project"""
    assert finder.get_compilable_sources([settings.sample_path]) == [
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

def test_finder_compilable_003(settings, finder):
    """finder.ScssInspector: Find recursively all compilable sources from
       sample project subdirectory"""
    assert finder.get_compilable_sources([os.path.join(settings.sample_path, 'components')]) == [
        os.path.join(settings.sample_path, 'components/twin_3.scss'),
        os.path.join(settings.sample_path, 'components/twin_2.scss'),
    ]
