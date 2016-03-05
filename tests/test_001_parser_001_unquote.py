# -*- coding: utf-8 -*-
import pytest


def test_parser_001_unquote1(settings, parser):
    """parser.ScssImportsParser: unquote case 1"""
    assert parser.strip_quotes("'foo'") == "foo"


def test_parser_002_unquote2(settings, parser):
    """parser.ScssImportsParser: unquote case 2"""
    assert parser.strip_quotes('"foo"') == "foo"


def test_parser_003_unquote3(settings, parser):
    """parser.ScssImportsParser: unquote case 3"""
    assert parser.strip_quotes("foo") == "foo"


def test_parser_004_unquote4(settings, parser):
    """parser.ScssImportsParser: unquote case 4"""
    assert parser.strip_quotes("'foo") == "'foo"
