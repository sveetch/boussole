# -*- coding: utf-8 -*-
import os
import pytest


def test_finder_changeextension_001(settings, finder):
    """finder.ScssFinder: Changing filename extension"""
    assert finder.change_extension("foo.scss", 'css') == "foo.css"


def test_finder_changeextension_002(settings, finder):
    """finder.ScssFinder: Changing filename extension"""
    assert finder.change_extension("foo.backup.scss", 'css') == "foo.backup.css"


def test_finder_changeextension_003(settings, finder):
    """finder.ScssFinder: Changing filename extension"""
    assert finder.change_extension("bar/foo.scss", 'css') == "bar/foo.css"


def test_finder_changeextension_004(settings, finder):
    """finder.ScssFinder: Changing filename extension"""
    assert finder.change_extension("/home/bar/foo.scss", 'css') == "/home/bar/foo.css"


def test_finder_changeextension_005(settings, finder):
    """finder.ScssFinder: Changing filename extension"""
    assert finder.change_extension("/home/bar/foo.backup.scss", 'css') == "/home/bar/foo.backup.css"
