import pytest


@pytest.mark.parametrize("source, new, hashid, expected", [
    ("foo.scss", "css", None, "foo.css"),
    ("foo.backup.scss", "css", None, "foo.backup.css"),
    ("bar/foo.scss", "css", None, "bar/foo.css"),
    ("/home/bar/foo.scss", "css", None, "/home/bar/foo.css"),
    ("/home/bar/foo.backup.scss", "css", None, "/home/bar/foo.backup.css"),
    ("foo.scss", "css", "hash", "foo.hash.css"),
    ("foo.backup.scss", "css", "hash", "foo.backup.hash.css"),
    ("/home/bar/foo.backup.scss", "css", "hash", "/home/bar/foo.backup.hash.css"),
])
def test_change_extension(settings, finder, source, new, hashid, expected):
    result = finder.change_extension(source, new, hashid)
    assert result == expected
