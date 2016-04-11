# -*- coding: utf-8 -*-
import os
import pytest

def test_001(settings, inspector):
    """inspector.ScssInspector: Sample doing depth imports"""
    sources = [
        os.path.join(settings.sample_path, 'main_depth_import-1.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-2.scss'),
        os.path.join(settings.sample_path, 'main_depth_import-3.scss'),
    ]
    inspector.inspect(*sources)

    # First depth level
    children = list(inspector.children(os.path.join(settings.sample_path, 'main_depth_import-1.scss')))
    assert children == [
        os.path.join(settings.sample_path, "_empty.scss"),
        os.path.join(settings.sample_path, "_vendor.scss"),
        os.path.join(settings.sample_path, "main_basic.scss"),
    ]

    parents = list(inspector.parents(os.path.join(settings.sample_path, 'main_depth_import-1.scss')))
    assert parents == [
        os.path.join(settings.sample_path, "main_depth_import-2.scss"),
        os.path.join(settings.sample_path, "main_depth_import-3.scss"),
    ]

    # Second depth level
    children = list(inspector.children(os.path.join(settings.sample_path, 'main_depth_import-2.scss')))
    assert children == [
        os.path.join(settings.sample_path, "main_depth_import-1.scss"),
        os.path.join(settings.sample_path, "_empty.scss"),
        os.path.join(settings.sample_path, "_vendor.scss"),
        os.path.join(settings.sample_path, "main_basic.scss"),
    ]

    parents = list(inspector.parents(os.path.join(settings.sample_path, 'main_depth_import-2.scss')))
    assert parents == [
        os.path.join(settings.sample_path, "main_depth_import-3.scss"),
    ]

    # Third depth level
    children = list(inspector.children(os.path.join(settings.sample_path, 'main_depth_import-3.scss')))
    assert children == [
        os.path.join(settings.sample_path, "main_depth_import-1.scss"),
        os.path.join(settings.sample_path, "main_depth_import-2.scss"),
        os.path.join(settings.sample_path, "_vendor.scss"),
        os.path.join(settings.sample_path, "main_basic.scss"),
        os.path.join(settings.sample_path, "_empty.scss"),
    ]

    parents = list(inspector.parents(os.path.join(settings.sample_path, 'main_depth_import-3.scss')))
    assert parents == []
