# -*- coding: utf-8 -*-
"""
JSON backend settings
=====================
"""
import json

from boussole.exceptions import SettingsLoadingError
from boussole.conf.base_backend import SettingsLoaderBase


class SettingsLoaderJson(SettingsLoaderBase):
    """
    JSON interface for settings
    """
    _default_filename = 'settings.json'

    def parse(self, filepath, content):
        """
        Parse opened settings content using JSON parser.

        Args:
            filepath (str): Settings object, depends from backend
            content (str): Settings content from opened file, depends from
                backend.

        Raises:
            SettingsLoadingError: If parser can not decode a valid JSON
                object.

        Returns:
            dict: Dictionnary containing parsed setting elements.

        """
        try:
            parsed = json.loads(content)
        except ValueError:
            msg = "No JSON object could be decoded from file: {}"
            raise SettingsLoadingError(msg.format(filepath))
        return parsed
