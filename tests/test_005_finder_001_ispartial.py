# -*- coding: utf-8 -*-
import os
import pytest


def test_finder_partial_001(settings, finder):
    """finder.ScssFinder: Simple filename"""
    allowed = finder.is_partial("foo.scss")
    assert allowed == False


def test_finder_partial_002(settings, finder):
    """finder.ScssFinder: Simple partial filename"""
    allowed = finder.is_partial("_foo.scss")
    assert allowed == True


def test_finder_partial_003(settings, finder):
    """finder.ScssFinder: Simple relative filename"""
    allowed = finder.is_partial("bar/foo.scss")
    assert allowed == False


def test_finder_partial_004(settings, finder):
    """finder.ScssFinder: Simple relative partial filename"""
    allowed = finder.is_partial("bar/_foo.scss")
    assert allowed == True


def test_finder_partial_005(settings, finder):
    """finder.ScssFinder: Simple relative filename again"""
    allowed = finder.is_partial("bar/plop/foo.scss")
    assert allowed == False


def test_finder_partial_006(settings, finder):
    """finder.ScssFinder: Simple relative partial filename again"""
    allowed = finder.is_partial("bar/plop/_foo.scss")
    assert allowed == True


def test_finder_partial_007(settings, finder):
    """finder.ScssFinder: Simple absolute filename"""
    allowed = finder.is_partial("/home/bar/foo.scss")
    assert allowed == False


def test_finder_partial_008(settings, finder):
    """finder.ScssFinder: Simple absolute partial filename"""
    allowed = finder.is_partial("/home/bar/_foo.scss")
    assert allowed == True
