# -*- coding: utf-8 -*-
"""
JSON settings backend
=====================
"""
import json

from boussole.exceptions import SettingsBackendError
from boussole.conf.base_backend import SettingsBackendBase


class SettingsBackendJson(SettingsBackendBase):
    """
    JSON backend for settings

    Attributes:
        _default_filename: Filename for settings file to load.
            Value is ``settings.json``.
        _kind_name: Backend format name.
            Value is ``json``.
        _file_extension: Default filename extension.
            Value is ``json``.
    """
    _default_filename = 'settings.json'
    _kind_name = 'json'
    _file_extension = 'json'

    def dump(self, content, filepath, indent=4):
        """
        Dump settings content to filepath.

        Args:
            content (str): Settings content.
            filepath (str): Settings file location.
        """
        with open(filepath, 'w') as fp:
            json.dump(content, fp, indent=indent)

    def parse(self, filepath, content):
        """
        Parse opened settings content using JSON parser.

        Args:
            filepath (str): Settings object, depends from backend
            content (str): Settings content from opened file, depends from
                backend.

        Raises:
            boussole.exceptions.SettingsBackendError: If parser can not decode
                a valid JSON object.

        Returns:
            dict: Dictionnary containing parsed setting elements.

        """
        try:
            parsed = json.loads(content)
        except ValueError:
            msg = "No JSON object could be decoded from file: {}"
            raise SettingsBackendError(msg.format(filepath))
        return parsed
