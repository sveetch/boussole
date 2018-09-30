# -*- coding: utf-8 -*-
import os
import io
from collections import OrderedDict

import pytest

from boussole.exceptions import SettingsDiscoveryError
from boussole.conf.discovery import Discover
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


class DummyTestBackend:
    """
    Dummy backend object just with object attributes required for
    discovering.
    """
    _default_filename = 'settings.dum'
    _kind_name = 'dummy'
    _file_extension = 'dum'


@pytest.mark.parametrize("backends,expected_engines,expected_exts,expected_filenames", [
    (
        [],
        (),
        (),
        (),
    ),
    (
        [DummyTestBackend],
        (
            (DummyTestBackend._kind_name, DummyTestBackend),
        ),
        (
            (DummyTestBackend._default_filename, DummyTestBackend._kind_name),
        ),
        (
            (DummyTestBackend._file_extension, DummyTestBackend._kind_name),
        ),
    ),
    (
        [SettingsBackendJson, SettingsBackendYaml, DummyTestBackend],
        (
            (SettingsBackendJson._kind_name, SettingsBackendJson),
            (SettingsBackendYaml._kind_name, SettingsBackendYaml),
            (DummyTestBackend._kind_name, DummyTestBackend),
        ),
        (
            (SettingsBackendJson._default_filename, SettingsBackendJson._kind_name),
            (SettingsBackendYaml._default_filename, SettingsBackendYaml._kind_name),
            (DummyTestBackend._default_filename, DummyTestBackend._kind_name),
        ),
        (
            (SettingsBackendJson._file_extension, SettingsBackendJson._kind_name),
            (SettingsBackendYaml._file_extension, SettingsBackendYaml._kind_name),
            (DummyTestBackend._file_extension, DummyTestBackend._kind_name),
        ),
    ),
])
def test_discover_scan_backends(backends, expected_engines, expected_exts,
                                expected_filenames):
    """
    Discover init engines from default backends
    """
    disco = Discover()

    engines, filenames, extensions = disco.scan_backends(backends)

    assert engines == OrderedDict(expected_engines)
    assert filenames == OrderedDict(expected_exts)
    assert extensions == OrderedDict(expected_filenames)


@pytest.mark.parametrize("filepath,kind,name", [
    ('foo.json', None, 'json'),
    ('foo.yml', None, 'yaml'),
    ('/home/foo.json', None, 'json'),
    ('/home/json/foo.yml', None, 'yaml'),
    ('.foo', 'json', 'json'),
    ('.foo', 'yaml', 'yaml'),
    ('/home/bar/.foo', 'yaml', 'yaml'),
    ('foo.bar', 'yaml', 'yaml'),
    ('foo.json', 'yaml', 'yaml'),
])
def test_get_backend_success(filepath, kind, name):
    """
    Discover backend from given filename and kind
    """
    disco = Discover([SettingsBackendJson, SettingsBackendYaml])
    backend = disco.get_engine(filepath, kind=kind)

    assert backend._kind_name == name


@pytest.mark.parametrize("filepath,kind", [
    ('.foo', None),
    ('foo.bar', None),
    ('foo.json.bar', None),
    ('/home/bar/.foo', None),
    ('foo.json', 'wrong'),
])
def test_get_backend_fail(filepath, kind):
    """
    Error on discovering backend from given filename
    """
    disco = Discover([SettingsBackendJson, SettingsBackendYaml])

    with pytest.raises(SettingsDiscoveryError):
        backend = disco.get_engine(filepath, kind=kind)


def test_search_empty():
    """
    Error if basedir and filepath are empty
    """
    disco = Discover()

    with pytest.raises(SettingsDiscoveryError):
        disco.search()


@pytest.mark.parametrize("datas", [
    # Absolute filepath to a json file
    ({
        'id': 'absolute_filepath_json',
        'filepath': 'BASEDIR_PREPEND/foo.json',
        'basedir': None,
        'kind': None,
        'fake_filename': 'foo.json',
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_engine': 'json'
    }),
    # Absolute filepath to a yaml file
    ({
        'id': 'absolute_filepath_yaml',
        'filepath': 'BASEDIR_PREPEND/foo.yml',
        'basedir': None,
        'kind': None,
        'fake_filename': 'foo.yml',
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_engine': 'yaml'
    }),
    # Absolute filepath to a json file and forced to json (although it's not
    # useful)
    ({
        'id': 'absolute_filepath_json_forced_to_json',
        'filepath': 'BASEDIR_PREPEND/foo.json',
        'basedir': None,
        'kind': 'json',
        'fake_filename': 'foo.json',
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_engine': 'json'
    }),
    # Absolute filepath to a json file but forced to yaml
    ({
        'id': 'absolute_filepath_json_forced_to_yaml',
        'filepath': 'BASEDIR_PREPEND/foo.json',
        'basedir': None,
        'kind': 'yaml',
        'fake_filename': 'foo.json',
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_engine': 'yaml'
    }),
    # Relative filepath to a json file and with basedir given
    ({
        'id': 'relative_filepath_json_with_basedir',
        'filepath': 'foo.json',
        'basedir': 'BASEDIR_PREPEND',
        'kind': 'json',
        'fake_filename': 'foo.json',
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_engine': 'json'
    }),
    # Given only basedir which contain a json file
    ({
        'id': 'no_filepath_with_basedir_json',
        'filepath': None,
        'basedir': 'BASEDIR_PREPEND',
        'kind': None,
        'fake_filename': SettingsBackendJson._default_filename,
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_engine': 'json'
    }),
    # Given only basedir which contain a yaml file
    ({
        'id': 'no_filepath_with_basedir_yaml',
        'filepath': None,
        'basedir': 'BASEDIR_PREPEND',
        'kind': None,
        'fake_filename': SettingsBackendYaml._default_filename,
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_engine': 'yaml'
    }),
])
def test_search_success(temp_builds_dir, datas):
    """
    Test discover search which should succeed
    """
    tmp_dirname = 'discovery_search_{}'.format(datas['id'])
    test_basedir = temp_builds_dir.join(tmp_dirname).strpath
    os.makedirs(test_basedir)

    # Prepend path with created temporary base directory since it can not
    # exists yet in parameter values
    if datas['filepath'] and datas['filepath'].startswith("BASEDIR_PREPEND"):
        datas['filepath'] = datas['filepath'].replace("BASEDIR_PREPEND", test_basedir)
    if datas['basedir'] and datas['basedir'].startswith("BASEDIR_PREPEND"):
        datas['basedir'] = datas['basedir'].replace("BASEDIR_PREPEND", test_basedir)

    # Create a dummy settings file in temp base directory
    if datas['fake_filename']:
        settings_filepath = os.path.join(test_basedir, datas['fake_filename'])
        with io.open(settings_filepath, 'w', encoding='utf-8') as f:
            result = f.write(u"""Dummy""")

    # Makes search
    disco = Discover(backends=datas['backends'])
    discovered_filepath, discovered_engine = disco.search(filepath=datas['filepath'],
                                                          basedir=datas['basedir'],
                                                          kind=datas['kind'])

    assert datas['expected_engine'] == discovered_engine._kind_name


@pytest.mark.parametrize("datas", [
    # Given only basedir which contain a json file but only yaml engine
    # is available
    # This one should be in a fail test: Relative filepath with an empty
    ({
        'id': 'no_filepath_with_basedir_nonavailable_engine',
        'filepath': None,
        'basedir': 'BASEDIR_PREPEND',
        'kind': None,
        'fake_filename': SettingsBackendJson._default_filename,
        'backends': [SettingsBackendYaml],
        'expected_exception': SettingsDiscoveryError
    }),
    # Relative filepath to a json file
    # This one should be in a fail test: Relative filepath with an empty
    # basedir cant work within tests since fake file in in temporary directory
    ({
        'id': 'relative_filepath_json',
        'filepath': 'foo.json',
        'basedir': None,
        'kind': None,
        'fake_filename': 'foo.json',
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_exception': SettingsDiscoveryError
    }),
    # Given basedir which contain a file with json extension but backend
    # explicitely specify yaml backend
    # This one should be in a fail test: giving an explicit backend name must
    # match the implicit filename.
    ({
        'id': 'with_basedir_and_backend',
        'filepath': None,
        'basedir': 'BASEDIR_PREPEND',
        'kind': 'yaml',
        'fake_filename': 'foo.json',
        'backends': [SettingsBackendJson, SettingsBackendYaml],
        'expected_exception': SettingsDiscoveryError
    }),
])
def test_search_fail(temp_builds_dir, datas):
    """
    Test discover search which should fails
    """
    tmp_dirname = 'discovery_search_{}'.format(datas['id'])
    test_basedir = temp_builds_dir.join(tmp_dirname).strpath
    os.makedirs(test_basedir)

    # Prepend path with created temporary base directory since it can not
    # exists yet in parameter values
    if datas['filepath'] and datas['filepath'].startswith("BASEDIR_PREPEND"):
        datas['filepath'] = datas['filepath'].replace("BASEDIR_PREPEND", test_basedir)
    if datas['basedir'] and datas['basedir'].startswith("BASEDIR_PREPEND"):
        datas['basedir'] = datas['basedir'].replace("BASEDIR_PREPEND", test_basedir)

    # Create a dummy settings file in temp base directory
    if datas['fake_filename']:
        settings_filepath = os.path.join(test_basedir, datas['fake_filename'])
        with io.open(settings_filepath, 'w', encoding='utf-8') as f:
            result = f.write(u"""Dummy""")

    # Makes search
    disco = Discover(backends=datas['backends'])
    with pytest.raises(datas['expected_exception']):
        discovered_filepath, discovered_engine = disco.search(filepath=datas['filepath'],
                                                            basedir=datas['basedir'],
                                                            kind=datas['kind'])
