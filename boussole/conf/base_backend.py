# -*- coding: utf-8 -*-
"""
Base settings backend
=====================

Backends are responsible to find settings file, parse it, load its values then
return a Settings object.

Backends inherit from :class:`boussole.conf.patcher` so they can patch each
loaded settings values following the settings manifest rules.

Actually the only backend available is JSON.

"""
import os

from boussole.exceptions import SettingsBackendError
from boussole.conf.model import Settings
from boussole.conf.patcher import SettingsPatcher


class SettingsBackendBase(SettingsPatcher):
    """
    Base project settings backend

    Args:
        basedir (str): Directory path where to search for settings filepath.

            Default is empty, meaning it will resolve path from current
            directory. Don't use an empty ``basedir`` attribute to load
            settings from non-absolute filepath.

            Given value will fill intial value for ``projectdir`` attribute.

    Attributes:
        _default_filename: Filename for settings file to load. Default to
            ``settings.txt`` but every backend should set their own filename.
    """
    _default_filename = 'settings.txt'

    def __init__(self, basedir=None):
        self.basedir = basedir or ''
        self.projectdir = self.basedir

    def parse_filepath(self, filepath=None):
        """
        Parse given filepath to split possible path directory from filename.

        * If path directory is empty, will use ``basedir`` attribute as base
          filepath;
        * If path directory is absolute, ignore ``basedir`` attribute;
        * If path directory is relative, join it to ``basedir`` attribute;

        Keyword Arguments:
            filepath (str): Filepath to use to search for settings file. Will
                use value from ``_default_filename`` class attribute if empty.

                If filepath contain a directory path, it will be splitted from
                filename and used as base directory (and update object
                ``basedir`` attribute).

        Returns:
            tuple: Separated path directory and filename.
        """
        filepath = filepath or self._default_filename

        path, filename = os.path.split(filepath)

        if not path:
            path = self.basedir
        elif not os.path.isabs(path):
            path = os.path.join(self.basedir, path)

        return os.path.normpath(path), filename

    def check_filepath(self, path, filename):
        """
        Check and return the final filepath to settings

        Args:
            path (str): Directory path where to search for settings file.
            filename (str): Filename to use to search for settings file.

        Raises:
            boussole.exceptions.SettingsBackendError: If determined filepath
                does not exists or is a directory.

        Returns:
            string: Settings file path, joining given path and filename.

        """
        settings_path = os.path.join(path, filename)

        if not os.path.exists(settings_path) or \
           not os.path.isfile(settings_path):
            msg = "Unable to find settings file: {}"
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

    def load(self, filepath=None):
        """
        Load settings file from given path and optionnal filepath.

        During path resolving, the ``projectdir`` is updated to the file path
        directory.

        Keyword Arguments:
            filepath (str): Filepath to the settings file.

        Returns:
            boussole.conf.model.Settings: Settings object with loaded elements.

        """
        self.projectdir, filename = self.parse_filepath(filepath)

        settings_path = self.check_filepath(self.projectdir, filename)

        parsed = self.parse(settings_path, self.open(settings_path))

        settings = self.clean(parsed)

        return Settings(initial=settings)
