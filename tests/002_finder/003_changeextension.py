# -*- coding: utf-8 -*-


def test_001(settings, finder):
    result = finder.change_extension("foo.scss", 'css')
    assert result == "foo.css"


def test_002(settings, finder):
    result = finder.change_extension("foo.backup.scss", 'css')
    assert result == "foo.backup.css"


def test_003(settings, finder):
    result = finder.change_extension("bar/foo.scss", 'css')
    assert result == "bar/foo.css"


def test_004(settings, finder):
    result = finder.change_extension("/home/bar/foo.scss", 'css')
    assert result == "/home/bar/foo.css"


def test_005(settings, finder):
    result = finder.change_extension("/home/bar/foo.backup.scss", 'css')
    assert result == "/home/bar/foo.backup.css"
