# -*- coding: utf-8 -*-
import os
import pytest


def test_001(settings, finder):
    """finder.ScssFinder: Get destination for simple filename"""
    assert finder.get_destination("foo.scss") == "foo.css"


def test_002(settings, finder):
    """finder.ScssFinder: Get destination for simple filename"""
    assert finder.get_destination("foo.bar.scss") == "foo.bar.css"


def test_003(settings, finder):
    """finder.ScssFinder: Get destination for relative filepath"""
    assert finder.get_destination("mip/foo.scss") == "mip/foo.css"


def test_004(settings, finder):
    """finder.ScssFinder: Get absolute destination for filepath"""
    result = finder.get_destination("foo.scss", targetdir="/home")
    assert result == "/home/foo.css"


def test_005(settings, finder):
    """finder.ScssFinder: Get absolute destination for filepath"""
    result = finder.get_destination("mip/foo.scss", targetdir="/home")
    assert result == "/home/mip/foo.css"


def test_006(settings, finder):
    """finder.ScssFinder: Wrong destination troubled with absolute filepath"""
    result = finder.get_destination("/etc/mip/foo.scss", targetdir="/home")
    assert result == "/etc/mip/foo.css"
