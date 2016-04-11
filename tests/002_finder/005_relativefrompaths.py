# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import FinderException


def test_001(finder):
    results = finder.get_relative_from_paths("/home/foo/plop", [
        "/home/foo",
        "/home/bar",
        "/etc",
    ])

    assert results == "plop"


def test_002(finder):
    results = finder.get_relative_from_paths("/etc/plop.plip", [
        "/home/foo",
        "/home/bar",
        "/etc",
    ])

    assert results == "plop.plip"


def test_003(finder):
    results = finder.get_relative_from_paths("/home/foo/plop", [
        "/home",
        "/home/foo",
        "/etc",
    ])

    assert results == "plop"


def test_004(finder):
    results = finder.get_relative_from_paths("/home/foo/plop", [
        "/home",
        "/home/foo",
        "/home/bar",
        "/etc/ping",
    ])

    assert results == "plop"


def test_005(finder):
    results = finder.get_relative_from_paths("/home/foo/plop", [
        "/home",
        "/home/foo",
        "/home/bar/pika",
        "/etc/ping",
    ])

    assert results == "plop"


def test_006(finder):
    results = finder.get_relative_from_paths("/home/foo/pika/plop", [
        "/home",
        "/home/foo",
        "/home/bar/pika",
        "/home/bar",
    ])

    assert results == "pika/plop"


def test_007(finder):
    results = finder.get_relative_from_paths("/home/foo/pika/plop", [
        "/etc",
        "/home/foo/pika",
        "/home/bar/pika",
        "/home/bar",
    ])

    assert results == "plop"


def test_008(finder):
    results = finder.get_relative_from_paths("/home/foo/pika/bim/bam/plop", [
        "/etc",
        "/home/foo/pika/bim/bam",
        "/home/foo/pika/bim/bom",
        "/home/bar/pika",
        "/home/bar",
    ])

    assert results == "plop"


def test_009(finder):
    """Unable to find relative path raise an exception"""
    with pytest.raises(FinderException):
        results = finder.get_relative_from_paths("/home/foo/pika/bim/bam/plop", [
            "/etc",
            "/home/foo/pika/bim/bom",
            "/home/bar/pika",
            "/home/bar",
        ])
