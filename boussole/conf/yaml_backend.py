# -*- coding: utf-8 -*-
"""
YAML settings backend
=====================
"""
import yaml
import pyaml

from boussole.exceptions import SettingsBackendError
from boussole.conf.base_backend import SettingsBackendBase


class SettingsBackendYaml(SettingsBackendBase):
    """
    YAML backend for settings

    Use PyYaml for parsing and pyaml for dumping.

    Attributes:
        _default_filename: Filename for settings file to load.
            Value is ``settings.yml``.
        _kind_name: Backend format name.
            Value is ``yaml``.
        _file_extension: Default filename extension.
            Value is ``yml``.
    """
    _default_filename = 'settings.yml'
    _kind_name = 'yaml'
    _file_extension = 'yml'

    def dump(self, content, filepath, indent=4):
        """
        Dump settings content to filepath.

        Args:
            content (str): Settings content.
            filepath (str): Settings file location.
        """
        with open(filepath, 'w') as fp:
            pyaml.dump(content, dst=fp, indent=indent)

    def parse(self, filepath, content):
        """
        Parse opened settings content using YAML parser.

        Args:
            filepath (str): Settings object, depends from backend
            content (str): Settings content from opened file, depends from
                backend.

        Raises:
            boussole.exceptions.SettingsBackendError: If parser can not decode
                a valid YAML object.

        Returns:
            dict: Dictionnary containing parsed setting elements.

        """
        try:
            parsed = yaml.load(content, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            msg = "No YAML object could be decoded from file: {}\n{}"
            raise SettingsBackendError(msg.format(filepath, exc))
        return parsed
