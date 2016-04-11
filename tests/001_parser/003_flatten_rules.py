# -*- coding: utf-8 -*-
import pytest


def test_001(settings, parser):
    """parser.ScssImportsParser: flatten_rules case 1"""
    rules = parser.flatten_rules([
        ('', '"foo"'),
    ])
    assert rules == ['foo']


def test_002(settings, parser):
    """parser.ScssImportsParser: flatten_rules case 2"""
    rules = parser.flatten_rules([
        ('', "'bar'"),
    ])
    assert rules == ['bar']


def test_003(settings, parser):
    """parser.ScssImportsParser: flatten_rules case 3"""
    rules = parser.flatten_rules([
        ('', "'bar'"),
        ('url', '"wrong"'),
        ('', '"cool", "plop"'),
        ('', '"wrong.css"'),
        ('', '"https://wrong"'),
    ])
    assert rules == [
        'bar',
        'cool', 'plop',
    ]
