# -*- coding: utf-8 -*-
import os
import pytest

def test_001_basic(settings, inspector):
    """inspector.ScssInspector: Looking for parents of basic sample"""
    sources = [
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
    ]
    sourcepath = os.path.join(settings.sample_path, 'main_basic.scss')

    inspector.inspect(*sources, library_paths=settings.libraries_fixture_paths)

    parents = list(inspector.parents(sourcepath))
    assert parents == [
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
    ]

def test_002_vendor(settings, inspector):
    """inspector.ScssInspector: Looking for parents of vendor component"""
    sources = [
        os.path.join(settings.sample_path, 'main_syntax.scss'),
        os.path.join(settings.sample_path, 'main_commented.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
        os.path.join(settings.sample_path, 'main_circular_0.scss'),
        os.path.join(settings.sample_path, 'main_circular_1.scss'),
        os.path.join(settings.sample_path, 'main_circular_2.scss'),
        os.path.join(settings.sample_path, 'main_circular_3.scss'),
        os.path.join(settings.sample_path, 'main_circular_4.scss'),
        os.path.join(settings.sample_path, 'main_circular_bridge.scss'),
        os.path.join(settings.sample_path, 'main_circular_5.scss'),
    ]
    sourcepath = os.path.join(settings.sample_path, '_vendor.scss')

    inspector.inspect(*sources, library_paths=settings.libraries_fixture_paths)

    parents = list(inspector.parents(sourcepath))
    assert parents == [
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_circular_4.scss'),
        os.path.join(settings.sample_path, 'main_circular_5.scss'),
        os.path.join(settings.sample_path, 'main_circular_bridge.scss'),
        os.path.join(settings.sample_path, 'main_commented.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'main_syntax.scss'),
        os.path.join(settings.sample_path, 'main_circular_3.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
    ]

def test_003_library(settings, inspector):
    """inspector.ScssInspector: Looking for parents of a library component"""
    sources = [
        os.path.join(settings.sample_path, 'main_syntax.scss'),
        os.path.join(settings.sample_path, 'main_commented.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
        os.path.join(settings.sample_path, 'main_circular_0.scss'),
        os.path.join(settings.sample_path, 'main_circular_1.scss'),
        os.path.join(settings.sample_path, 'main_circular_2.scss'),
        os.path.join(settings.sample_path, 'main_circular_3.scss'),
        os.path.join(settings.sample_path, 'main_circular_4.scss'),
        os.path.join(settings.sample_path, 'main_circular_bridge.scss'),
        os.path.join(settings.sample_path, 'main_circular_5.scss'),
    ]
    sourcepath = os.path.join(settings.lib1_path, 'components/_panels.scss')

    inspector.inspect(*sources, library_paths=settings.libraries_fixture_paths)

    parents = list(inspector.parents(sourcepath))
    assert parents == [
        os.path.join(settings.lib1_path, 'library_1_fullstack.scss'),
        os.path.join(settings.sample_path, 'main_using_libs.scss'),
    ]
