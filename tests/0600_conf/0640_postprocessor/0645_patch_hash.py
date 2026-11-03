import json

import pytest

from boussole.conf.post_processor import SettingsPostProcessor
from boussole.conf.json_backend import SettingsBackendJson


@pytest.mark.parametrize("value, expected", [
    (False, None),
    (None, None),
    ("foo", "foo"),
    (":", ":"),
    (":foo", ":foo"),
    ("blake2", "blake2"),
])
def test_postprocessor_patch_hash_suffix_nonhash(value, expected):
    """
    Post processor should Coerce value to None for empty value or leave it unchanged
    for non valid hash engine names.
    """
    processor = SettingsPostProcessor()

    result = processor._patch_hash_suffix({}, "DUMMY_NAME", value)
    assert result == expected


@pytest.mark.parametrize("value", [True, ":blake2"])
def test_postprocessor_patch_hash_suffix_blake2(value):
    """
    Post processor should build a hash with Blake2.

    We don't assert on value content since hash is almost unique and we can not know it.
    """
    processor = SettingsPostProcessor()

    result = processor._patch_hash_suffix({}, "DUMMY_NAME", value)
    assert len(result) == 20


@pytest.mark.parametrize("value", [":uuid"])
def test_postprocessor_patch_hash_suffix_uuid(value):
    """
    Post processor should build a hash with UUID.

    We don't assert on value content since hash is unique and we can not know it.
    """
    processor = SettingsPostProcessor()

    result = processor._patch_hash_suffix({}, "DUMMY_NAME", value)
    assert len(result) == 32


def test_settings_hash_filling(tmp_path, settings):
    """
    When HASH_SUFFIX is enabled (with default hash engine), the setting should be
    filled with a hash from blake2.
    """
    settings_sample = tmp_path / "boussole.json"

    # Required to pass validations
    d = tmp_path / "css"
    d.mkdir()

    settings_sample.write_text(
        json.dumps({
            "SOURCES_PATH": ".",
            "TARGET_PATH": "./css",
            "HASH_SUFFIX": True,
        })
    )

    backend = SettingsBackendJson(basedir=tmp_path)

    settings_object = backend.load(filepath="boussole.json")

    # Only check integrity, not the value since it cant really be previewed
    assert isinstance(settings_object.HASH_SUFFIX, str) is True
    assert len(settings_object.HASH_SUFFIX) == 20
