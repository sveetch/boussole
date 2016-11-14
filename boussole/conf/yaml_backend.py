# -*- coding: utf-8 -*-
"""
YAML settings backend
=====================
"""
import yaml

from boussole.exceptions import SettingsBackendError
from boussole.conf.base_backend import SettingsBackendBase


class SettingsBackendYaml(SettingsBackendBase):
    """
    YAML backend for settings
    """
    _default_filename = 'settings.yaml' #: Default filename
    _kind_name = 'yaml' #: Backend format name

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
            parsed = yaml.load(content)
        except yaml.YAMLError as exc:
            msg = "No YAML object could be decoded from file: {}\n{}"
            raise SettingsBackendError(msg.format(filepath, exc))
        return parsed
