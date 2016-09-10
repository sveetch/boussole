# -*- coding: utf-8 -*-
import os
import pytest


def test_001(settings, inspector):
    """Basic sample in confined space"""
    sourcepath = os.path.join(settings.sample_path, 'main_basic.scss')
    inspector.inspect(sourcepath)

    children = inspector.children(sourcepath)
    assert children == set([
        os.path.join(settings.sample_path, '_empty.scss'),
        os.path.join(settings.sample_path, '_vendor.scss'),
    ])

    parents = inspector.parents(sourcepath)
    assert parents == set([])


def test_encoding(settings, inspector):
    """Inspecting files with unicode, initially related to issue #17"""
    sourcepath = os.path.join(settings.sample_path, 'main_encoding.scss')
    inspector.inspect(sourcepath)

    children = inspector.children(sourcepath)
    assert children == set([
        os.path.join(settings.sample_path, '_vendor.scss'),
        os.path.join(settings.sample_path, 'components/_encoding.scss'),
    ])

    parents = inspector.parents(sourcepath)
    assert parents == set([])
