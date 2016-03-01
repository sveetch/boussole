# -*- coding: utf-8 -*-
import os
import pytest


def test_inspector_001_basic(settings, inspector):
    """inspector.ScssInspector: Dependancies of basic sample"""
    sourcepath = os.path.join(settings.sample_path, 'main_basic.scss')
    
    inspector.inspect(sourcepath)
    
    assert list(inspector.dependancies(sourcepath)) == [
        os.path.join(settings.sample_path, '_empty.scss'),
        os.path.join(settings.sample_path, '_vendor.scss'), 
    ]
