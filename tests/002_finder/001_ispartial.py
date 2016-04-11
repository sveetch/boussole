# -*- coding: utf-8 -*-
import os
import pytest


def test_001(settings, finder):
    """finder.ScssFinder: Simple filename"""
    partial = finder.is_partial("foo.scss")
    assert partial == False


def test_002(settings, finder):
    """finder.ScssFinder: Simple partial filename"""
    partial = finder.is_partial("_foo.scss")
    assert partial == True


def test_003(settings, finder):
    """finder.ScssFinder: Simple relative filename"""
    partial = finder.is_partial("bar/foo.scss")
    assert partial == False


def test_004(settings, finder):
    """finder.ScssFinder: Simple relative partial filename"""
    partial = finder.is_partial("bar/_foo.scss")
    assert partial == True


def test_005(settings, finder):
    """finder.ScssFinder: Simple relative filename again"""
    partial = finder.is_partial("bar/plop/foo.scss")
    assert partial == False


def test_006(settings, finder):
    """finder.ScssFinder: Simple relative partial filename again"""
    partial = finder.is_partial("bar/plop/_foo.scss")
    assert partial == True


def test_007(settings, finder):
    """finder.ScssFinder: Simple absolute filename"""
    partial = finder.is_partial("/home/bar/foo.scss")
    assert partial == False


def test_008(settings, finder):
    """finder.ScssFinder: Simple absolute partial filename"""
    partial = finder.is_partial("/home/bar/_foo.scss")
    assert partial == True
