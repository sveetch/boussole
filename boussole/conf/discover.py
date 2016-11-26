# -*- coding: utf-8 -*-
"""
Backend discover
================

"""
import os

from boussole.exceptions import SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


def get_backend(filepath, kind=None):
    """
    From given filepath try to discover which backend format to use.

    Discovering is pretty naive as it find format from file extension.

    Args:
        filepath (str): Settings filepath or filename.

    Keyword Arguments:
        kind (str): A format name to enforce a specific backend. Can be either
            ``json`` or ``yaml``. Default to ``None``.

    Raises:
        boussole.exceptions.SettingsBackendError: If extension is unknowed or
            if given format name is unknowed.

    Returns:
        object: Backend object.

    """
    engines = {
        'json': SettingsBackendJson,
        'yaml': SettingsBackendYaml,
    }
    extensions = {
        'json': 'json',
        'yml': 'yaml',
    }

    if not kind:
        extension = os.path.splitext(filepath)[1]
        if not extension:
            msg = ("Unable to discover settings format from an empty file "
                   "extension: {}")
            raise SettingsBackendError(msg.format(filepath))
        elif extension[1:] not in extensions:
            msg = ("Settings file extension is unknowed from available "
                   "backends: {}")
            raise SettingsBackendError(msg.format(filepath))
        kind = extensions[extension[1:]]
    elif kind not in engines:
        msg = "Given settings format is unknowed: {}"
        raise SettingsBackendError(msg.format(kind))

    return engines[kind]
