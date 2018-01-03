# -*- coding: utf-8 -*-
import os
import pytest

from boussole.parser import ScssImportsParser, SassImportsParser


@pytest.mark.parametrize('filepath,expected_parser', [
    ('foo', "scss"),
    ('.foo', "scss"),
    ('foo.scss', "scss"),
    ('foo.sass', "sass"),
    ('dumb/foo.scss', "scss"),
    ('/home/dumb/foo.scss', "scss"),
    ('/home/dumb/foo.sass', "sass"),
])
def test_get_parser(inspector, filepath, expected_parser):
    """
    Check
    """
    result = inspector.get_parser(filepath)

    assert result.syntax == expected_parser
