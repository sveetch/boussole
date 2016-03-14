# -*- coding: utf-8 -*-
"""
Base backend settings
=====================
"""
import os

from boussole.exceptions import SettingsLoadingError


class SettingsLoaderBase(object):
    """
    Base project settings backend

    Backends are responsible to correctly implement methods from their needs.

    Attributes:
        _default_filename: Filename for settings file to load. Default to
            ``settings.txt`` but every backend should set their own filename.
    """
    _default_filename = 'settings.txt'

    def get_filepath(self, path, filename=None):
        """
        Check and return the final filepath to settings

        Args:
            path (str): Directory path where to search for settings file.

        Keyword Arguments:
            filename (str): Filename to use to search for settings file. Will
                use ``_default_filename`` value if empty.

        Raises:
            SettingsLoadingError: If determined filepath does not exists or is
                a directory.

        Returns:
            string: Settings file path

        """
        filename = filename or self._default_filename
        settings_path = os.path.join(path, filename)

        if not os.path.exists(settings_path) or \
           not os.path.isfile(settings_path):
            msg = "Unable to load settings file: {}"
            raise SettingsLoadingError(msg.format(settings_path))

        return settings_path

    def open(self, filepath):
        """
        Open settings backend to return its content

        Args:
            filepath (str): Settings object, depends from backend

        Returns:
            string: Settings file content.

        """
        with open(filepath) as fp:
            content = fp.read()
        return content

    def parse(self, filepath, content):
        """
        Parse opened settings content

        Base method do nothing because parsing is dependent from backend.

        Args:
            filepath (str): Settings object, depends from backend
            content (str): Settings content from opened file, depends from
                backend.

        Returns:
            dict: Dictionnary containing parsed setting elements.

        """
        return {}

    def clean(self, settings):
        """
        Clean given settings for backend needs.

        Args:
            dict: Loaded settings.

        Returns:
            dict: Settings object cleaned.

        """
        return settings

    def load(self, path, filename=None):
        """
        Pretend to load the settings file from given path and optionnal
        filename.

        Final backend settings interface have to implement the final loading.

        Args:
            path (str): Directory path where to search for settings file.

        Keyword Arguments:
            filename (str): Filename to use to search for settings file. Will
            use ``_default_filename`` value if empty.

        Returns:
            str: File path.

        """
        settings_path = self.get_filepath(path, filename)

        parsed = self.parse(settings_path, self.open(settings_path))

        settings = self.clean(parsed)

        return settings
