# -*- coding: utf-8 -*-
import os
import pytest

def test_001(settings, inspector):
    """inspector.ScssInspector: Ensure inspection maps are well reset"""
    sourcepath = os.path.join(settings.sample_path, 'main_basic.scss')

    inspector.inspect(sourcepath)

    inspector.reset()

    assert inspector._CHILDREN_MAP  == {}
    assert inspector._PARENTS_MAP == {}
    assert inspector.children(sourcepath) == set([])
    assert inspector.parents(sourcepath)  == set([])
