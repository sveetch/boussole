# -*- coding: utf-8 -*-
import pytest


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
    Inspector should guess the correct parser name from filename.
    """
    result = inspector.get_parser(filepath)

    assert result.syntax == expected_parser
