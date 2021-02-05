import pytest

from boussole.utils import match_path


@pytest.mark.parametrize("path, included, excluded, case_sensitive, expected", [
    (
        "/home/plop/foobar.py",
        {"*.py"},
        {"*.PY"},
        True,
        True,
    ),
    (
        "/home/plop/foobar.PY",
        {"*.py"},
        {"*.PY"},
        True,
        False,
    ),
    (
        "/home/plop/foobar.py",
        {"*.py"},
        {"*.txt"},
        False,
        True,
    ),
    (
        "/home/plop/foobar.PY",
        {"*.py"},
        {"*.txt"},
        False,
        True,
    ),
    (
        "/home/plop/foobar.txt",
        {"*.py"},
        {"*.txt"},
        False,
        False,
    ),
    (
        "/home/plop/",
        {"*.py"},
        {"*.txt"},
        False,
        False,
    ),
    (
        "/home/plop/",
        {"*.py"},
        {"*.txt"},
        True,
        False,
    ),
])
def test_match_path_success(path, included, excluded, case_sensitive, expected):
    assert match_path(path, included, excluded, case_sensitive) is expected


@pytest.mark.parametrize("path, included, excluded, case_sensitive", [
    (
        "/home/plop/foobar.py",
        {"*.py"},
        {"*.py"},
        True,
    ),
    (
        "/home/plop/foobar.py",
        {"*.py"},
        {"*.PY"},
        False,
    ),
])
def test_match_path_fail(path, included, excluded, case_sensitive):
    with pytest.raises(ValueError):
        match_path(path, included, excluded, case_sensitive)
