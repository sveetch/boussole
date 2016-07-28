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
    children = inspector.children(os.path.join(settings.sample_path, 'main_depth_import-1.scss'))
    assert children == set([
        os.path.join(settings.sample_path, "_empty.scss"),
        os.path.join(settings.sample_path, "_vendor.scss"),
        os.path.join(settings.sample_path, "main_basic.scss"),
    ])

    parents = inspector.parents(os.path.join(settings.sample_path, 'main_depth_import-1.scss'))
    assert parents == set([
        os.path.join(settings.sample_path, "main_depth_import-2.scss"),
        os.path.join(settings.sample_path, "main_depth_import-3.scss"),
    ])

    # Second depth level
    children = inspector.children(os.path.join(settings.sample_path, 'main_depth_import-2.scss'))
    assert children == set([
        os.path.join(settings.sample_path, "main_depth_import-1.scss"),
        os.path.join(settings.sample_path, "_empty.scss"),
        os.path.join(settings.sample_path, "_vendor.scss"),
        os.path.join(settings.sample_path, "main_basic.scss"),
    ])

    parents = inspector.parents(os.path.join(settings.sample_path, 'main_depth_import-2.scss'))
    assert parents == set([
        os.path.join(settings.sample_path, "main_depth_import-3.scss"),
    ])

    # Third depth level
    children = inspector.children(os.path.join(settings.sample_path, 'main_depth_import-3.scss'))
    assert children == set([
        os.path.join(settings.sample_path, "main_depth_import-1.scss"),
        os.path.join(settings.sample_path, "main_depth_import-2.scss"),
        os.path.join(settings.sample_path, "_vendor.scss"),
        os.path.join(settings.sample_path, "main_basic.scss"),
        os.path.join(settings.sample_path, "_empty.scss"),
    ])

    parents = inspector.parents(os.path.join(settings.sample_path, 'main_depth_import-3.scss'))
    assert parents == set([])
