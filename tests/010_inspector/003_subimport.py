# -*- coding: utf-8 -*-
import os
import pytest

def test_001(settings, inspector):
    """inspector.ScssInspector: Sub import dependencies"""
    sourcepath = os.path.join(settings.sample_path, 'main_with_subimports.scss')
    sources = [
        sourcepath,
    ]

    inspector.inspect(*sources)

    import json

    results = inspector.children(sourcepath)

    assert results == set([
        os.path.join(settings.sample_path, "_empty.scss"),
        os.path.join(settings.sample_path, "_vendor.scss"),
        os.path.join(settings.sample_path, "components/_webfont.scss"),
        os.path.join(settings.sample_path, "main_basic.scss"),
        os.path.join(settings.sample_path, "components/_webfont_icons.scss"),
    ])

    assert inspector.parents(sourcepath)  == set([])
