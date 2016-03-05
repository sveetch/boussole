# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import InvalidImportRule

def test_inspector_libs_001_empty(settings, inspector):
    """inspector.ScssInspector: Some lib components used but no given library"""
    sourcepath = os.path.join(settings.sample_path, 'main_using_libs.scss')
    
    sources = [
        sourcepath,
    ]
    
    with pytest.raises(InvalidImportRule):
        inspector.inspect(*sources)

def test_inspector_libs_002_children(settings, inspector):
    """inspector.ScssInspector: Children with some lib components used"""
    sourcepath = os.path.join(settings.sample_path, 'main_using_libs.scss')
    
    sources = [
        sourcepath,
    ]
    
    inspector.inspect(*sources, library_paths=settings.libraries_fixture_paths)

    children = list(inspector.children(sourcepath))
    assert children == [
        os.path.join(settings.sample_path, '_empty.scss'),
        os.path.join(settings.lib1_path, 'settings/_sample.scss'),
        os.path.join(settings.sample_path, '_vendor.scss'),
        os.path.join(settings.lib2_path, 'addons/_some_addon.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.lib1_path, 'components/_panels.scss'),
        os.path.join(settings.lib1_path, 'library_1_fullstack.scss'),
        os.path.join(settings.lib2_path, 'addons/_another_addon.scss'),
        os.path.join(settings.lib1_path, 'components/_sections.scss'),
        os.path.join(settings.sample_path, 'components/_webfont_icons.scss'),
        os.path.join(settings.sample_path, 'components/_webfont.scss'),
    ]
