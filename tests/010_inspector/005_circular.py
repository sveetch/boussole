# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import CircularImport

def test_self(settings, inspector):
    """inspector.ScssInspector: Ensure self import is detected"""
    sourcepath_0 = os.path.join(settings.sample_path, 'main_circular_0.scss')

    sources = [
        os.path.join(settings.sample_path, 'main_basic.scss'),
        sourcepath_0,
    ]

    inspector.inspect(*sources)

    with pytest.raises(CircularImport):
        children = list(inspector.children(sourcepath_0))

    with pytest.raises(CircularImport):
        parents = list(inspector.parents(sourcepath_0))

def test_direct(settings, inspector):
    """inspector.ScssInspector: Ensure direct circular imports are detected"""
    sourcepath_1 = os.path.join(settings.sample_path, 'main_circular_1.scss')
    sourcepath_2 = os.path.join(settings.sample_path, 'main_circular_2.scss')

    sources = [
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        sourcepath_1,
        sourcepath_2,
    ]

    inspector.inspect(*sources)

    with pytest.raises(CircularImport):
        children = list(inspector.children(sourcepath_1))

    with pytest.raises(CircularImport):
        parents = list(inspector.parents(sourcepath_1))

    with pytest.raises(CircularImport):
        children = list(inspector.children(sourcepath_2))

    with pytest.raises(CircularImport):
        parents = list(inspector.parents(sourcepath_2))


def test_indirect(settings, inspector):
    """inspector.ScssInspector: Ensure indirect circular imports are detected"""
    sourcepath_3 = os.path.join(settings.sample_path, 'main_circular_3.scss')
    sourcepath_4 = os.path.join(settings.sample_path, 'main_circular_4.scss')
    sourcepath_bridge = os.path.join(settings.sample_path, 'main_circular_bridge.scss')
    sourcepath_5 = os.path.join(settings.sample_path, 'main_circular_5.scss')

    sources = [
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        sourcepath_3,
        sourcepath_4,
        sourcepath_bridge,
        sourcepath_5,
    ]

    inspector.inspect(*sources)

    # Case 3
    with pytest.raises(CircularImport):
        children = list(inspector.children(sourcepath_3))

    with pytest.raises(CircularImport):
        parents = list(inspector.parents(sourcepath_3))

    # Case 4
    with pytest.raises(CircularImport):
        children = list(inspector.children(sourcepath_4))

    with pytest.raises(CircularImport):
        parents = list(inspector.parents(sourcepath_4))

    # Bridge
    with pytest.raises(CircularImport):
        children = list(inspector.children(sourcepath_bridge))

    with pytest.raises(CircularImport):
        parents = list(inspector.parents(sourcepath_bridge))


# NOTE: Disabled until i find a way to detected circular imports not
# directly involved by the source"""
#def test_004_subimport(settings, inspector):
    #"""inspector.ScssInspector: Ensure sub circular imports are detected"""
    #sourcepath_3 = os.path.join(settings.sample_path, 'main_circular_3.scss')
    #sourcepath_4 = os.path.join(settings.sample_path, 'main_circular_4.scss')
    #sourcepath_bridge = os.path.join(settings.sample_path, 'main_circular_bridge.scss')
    #sourcepath_5 = os.path.join(settings.sample_path, 'main_circular_5.scss')

    #sources = [
        #os.path.join(settings.sample_path, 'main_basic.scss'),
        #os.path.join(settings.sample_path, 'main_with_subimports.scss'),
        #sourcepath_3,
        #sourcepath_4,
        #sourcepath_bridge,
        #sourcepath_5,
    #]

    #inspector.inspect(*sources)

    ## Case 5
    #with pytest.raises(CircularImport):
        #children = list(inspector.children(sourcepath_5))

    #with pytest.raises(CircularImport):
        #parents = list(inspector.parents(sourcepath_5))
