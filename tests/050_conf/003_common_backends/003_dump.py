# -*- coding: utf-8 -*-
import os

import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


@pytest.mark.parametrize("backend_engine,attempted", [
    (
        SettingsBackendJson,
        ("""{\n"""
         """    "donald": [\n"""
         """        "riri", \n"""
         """        "fifi", \n"""
         """        "loulou"\n"""
         """    ], \n"""
         """    "foo": "bar"\n"""
         """}""")
    ),
    (
        SettingsBackendYaml,
        ("""donald:\n"""
         """    - riri\n"""
         """    - fifi\n"""
         """    - loulou\n"""
         """foo: bar\n""")
    ),
])
def test_ok(temp_builds_dir, backend_engine, attempted):
    """Dump data from backend"""
    tmp_dirname = 'backend_dump_{}'.format(backend_engine._kind_name)
    settings_filename = backend_engine._default_filename
    basedir = temp_builds_dir.join(tmp_dirname).strpath

    os.makedirs(basedir)

    destination = os.path.join(basedir, settings_filename)

    content = {
        'foo': 'bar',
        'donald': ['riri', 'fifi', 'loulou']
    }

    backend = backend_engine()

    backend.dump(content, filepath=destination)

    with open(destination, "r") as fp:
        content = fp.read()

    assert content == attempted
