# -*- coding: utf-8 -*-
import os
import pytest


def test_finder_partial_001(settings, finder):
    """finder.ScssFinder: Simple filename"""
    partial = finder.is_partial("foo.scss")
    assert partial == False


def test_finder_partial_002(settings, finder):
    """finder.ScssFinder: Simple partial filename"""
    partial = finder.is_partial("_foo.scss")
    assert partial == True


def test_finder_partial_003(settings, finder):
    """finder.ScssFinder: Simple relative filename"""
    partial = finder.is_partial("bar/foo.scss")
    assert partial == False


def test_finder_partial_004(settings, finder):
    """finder.ScssFinder: Simple relative partial filename"""
    partial = finder.is_partial("bar/_foo.scss")
    assert partial == True


def test_finder_partial_005(settings, finder):
    """finder.ScssFinder: Simple relative filename again"""
    partial = finder.is_partial("bar/plop/foo.scss")
    assert partial == False


def test_finder_partial_006(settings, finder):
    """finder.ScssFinder: Simple relative partial filename again"""
    partial = finder.is_partial("bar/plop/_foo.scss")
    assert partial == True


def test_finder_partial_007(settings, finder):
    """finder.ScssFinder: Simple absolute filename"""
    partial = finder.is_partial("/home/bar/foo.scss")
    assert partial == False


def test_finder_partial_008(settings, finder):
    """finder.ScssFinder: Simple absolute partial filename"""
    partial = finder.is_partial("/home/bar/_foo.scss")
    assert partial == True
