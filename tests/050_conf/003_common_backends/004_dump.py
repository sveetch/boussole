# -*- coding: utf-8 -*-
import os
import json
import yaml

import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


@pytest.mark.parametrize("backend_engine,loader", [
    (
        SettingsBackendJson,
        json.loads
    ),
    (
        SettingsBackendYaml,
        yaml.load
    ),
])
def test_ok(temp_builds_dir, backend_engine, loader):
    """Dump data from backend"""
    tmp_dirname = 'backend_dump_{}'.format(backend_engine._kind_name)
    settings_filename = backend_engine._default_filename
    basedir = temp_builds_dir.join(tmp_dirname).strpath

    os.makedirs(basedir)

    destination = os.path.join(basedir, settings_filename)

    datas = {
        'foo': 'bar',
        'donald': ['riri', 'fifi', 'loulou']
    }

    backend = backend_engine()

    backend.dump(datas, filepath=destination)

    with open(destination, "r") as fp:
        content = fp.read()

    # Compare initial datas dict with parsed content from dumped datas file
    assert datas == loader(content)
