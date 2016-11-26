# -*- coding: utf-8 -*-
import os

import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


@pytest.mark.parametrize("context,name,klass", [
    ({}, 'json', SettingsBackendJson),
    ({'backend_name': 'yaml'}, 'yaml', SettingsBackendYaml),
    ({'backend_name': 'json'}, 'json', SettingsBackendJson),
])
def test_init(projectstarter, context, name, klass):
    """Default backend"""
    p = projectstarter(**context)

    assert p.backend_name == name
    assert isinstance(p.backend_engine, klass) == True


@pytest.mark.parametrize("name,klass", [
    ('json', SettingsBackendJson),
    ('yaml', SettingsBackendYaml),
])
def test_get_backend(projectstarter, name, klass):
    """Get backend"""
    p = projectstarter()

    engine = p.get_backend_engine(name)

    assert isinstance(engine, klass) == True


def test_error(projectstarter):
    """Error on default backend"""
    with pytest.raises(SettingsBackendError):
        projectstarter(backend_name='wrong')
