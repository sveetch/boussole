# -*- coding: utf-8 -*-
import pytest

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


@pytest.mark.parametrize("name,klass", [
    ('json', SettingsBackendJson),
    ('yaml', SettingsBackendYaml),
    ('json', SettingsBackendJson),
])
def test_init(projectstarter, name, klass):
    """
    Default backend
    """
    p = projectstarter(name)

    assert p.backend_name == name
    assert isinstance(p.backend_engine, klass)


@pytest.mark.parametrize("name,klass", [
    ('json', SettingsBackendJson),
    ('yaml', SettingsBackendYaml),
])
def test_get_backend(projectstarter, name, klass):
    """
    Get backend
    """
    p = projectstarter(name)

    engine = p.get_backend_engine(name)

    assert isinstance(engine, klass)


def test_error(projectstarter):
    """
    Error on default backend
    """
    with pytest.raises(SettingsBackendError):
        projectstarter(backend_name='wrong')
