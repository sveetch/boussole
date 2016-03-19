# -*- coding: utf-8 -*-
"""
Base settings backend
=====================

Backends are responsible to find settings file, parse it, load its values then
return a Settings object.

Each loaded setting values can be patched following settings manifest rules,
see :class:`boussole.conf.patcher`.

"""
import os

from boussole.exceptions import SettingsBackendError
from boussole.conf.model import Settings
from boussole.conf.patcher import SettingsPatcher


class SettingsBackendBase(SettingsPatcher):
    """
    Base project settings backend

    Args:
        basedir (str): Directory path where to search for settings file.
            Default is empty, meaning it will resolve path from current
            directory. You are advised to avoid this kind of usage and allways
            provide an absolute base directory.

    Attributes:
        _default_filename: Filename for settings file to load. Default to
            ``settings.txt`` but every backend should set their own filename.
    """
    _default_filename = 'settings.txt'

    def __init__(self, basedir=None):
        self.basedir = basedir or ''

    def get_filepath(self, path, filename=None):
        """
        Check and return the final filepath to settings

        Args:
            path (str): Directory path where to search for settings file.

        Keyword Arguments:
            filename (str): Filename to use to search for settings file. Will
                use ``_default_filename`` value if empty.

        Raises:
            boussole.exceptions.SettingsBackendError: If determined filepath
                does not exists or is a directory.

        Returns:
            string: Settings file path

        """
        filename = filename or self._default_filename
        settings_path = os.path.join(path, filename)

        if not os.path.exists(settings_path) or \
           not os.path.isfile(settings_path):
            msg = "Unable to load settings file: {}"
            raise SettingsBackendError(msg.format(settings_path))

        return settings_path

    def open(self, filepath):
        """
        Open settings backend to return its content

        Args:
            filepath (str): Settings object, depends from backend

        Returns:
            string: File content.

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

        Default backend only apply available patchs.

        Args:
            dict: Loaded settings.

        Returns:
            dict: Settings object cleaned.

        """
        return self.patch(settings)

    def load(self, filename=None):
        """
        Pretend to load the settings file from given path and optionnal
        filename.

        Final backend settings interface have to implement the final loading.

        Keyword Arguments:
            filename (str): Filename to use to search for settings file. Will
                use value from ``_default_filename`` class attribute if empty.

        Returns:
            boussole.conf.model.Settings: Settings object with loaded elements.

        """
        settings_path = self.get_filepath(self.basedir, filename)

        parsed = self.parse(settings_path, self.open(settings_path))

        settings = self.clean(parsed)

        return Settings(initial=settings)
