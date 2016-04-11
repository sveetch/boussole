# -*- coding: utf-8 -*-
import os
import pytest

# Temporary
#ALL_SOURCES = [
    #os.path.join(settings.sample_path, 'main_syntax.scss'),
    #os.path.join(settings.sample_path, 'main_commented.scss'),
    #os.path.join(settings.sample_path, 'main_basic.scss'),
    #os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
    #os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
    #os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
    #os.path.join(settings.sample_path, 'main_with_subimports.scss'),
    #os.path.join(settings.sample_path, 'main_using_libs.scss'),
    #os.path.join(settings.sample_path, 'main_circular_0.scss'),
    #os.path.join(settings.sample_path, 'main_circular_1.scss'),
    #os.path.join(settings.sample_path, 'main_circular_2.scss'),
    #os.path.join(settings.sample_path, 'main_circular_3.scss'),
    #os.path.join(settings.sample_path, 'main_circular_4.scss'),
    #os.path.join(settings.sample_path, 'main_circular_bridge.scss'),
    #os.path.join(settings.sample_path, 'main_circular_5.scss'),
#]


def test_001(settings, inspector):
    """inspector.ScssInspector: Basic sample in confined space"""
    sourcepath = os.path.join(settings.sample_path, 'main_basic.scss')
    inspector.inspect(sourcepath)

    children = list(inspector.children(sourcepath))
    assert children == [
        os.path.join(settings.sample_path, '_empty.scss'),
        os.path.join(settings.sample_path, '_vendor.scss'),
    ]

    parents = list(inspector.parents(sourcepath))
    assert parents == []
