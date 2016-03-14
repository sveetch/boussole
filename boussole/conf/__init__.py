# -*- coding: utf-8 -*-
"""
Project configuration
=====================
"""


# Default values for initial settings object
DEFAULT_SETTINGS = {
    'COMPILER_ARGS': [],
    'LIBRARY_PATHS': [],
    'SOURCES_PATHS': [],
    'TARGET_PATH': None,
}


class Settings(object):
    """
    Settings object

    Class init method fills object attributes from either given default
    settings if given or the default ones from ``DEFAULT_SETTINGS``.

    Todo:
        Add a filter method to process "_enabled_names" to avoid naming
        convention errors in backends ? (Although they are dependent from
        developer, not users)

    Keyword Arguments:
        settings (dict): A dictionnary of settings for starting values.
    """
    def __init__(self, *args, **kwargs):
        self._settings = self.clean(kwargs.get('settings', DEFAULT_SETTINGS))
        self.update(self._settings)

    def clean(self, settings):
        """
        Clean given settings to keep only key names available in
        ``DEFAULT_SETTINGS``.

        Args:
            dict: Loaded settings.

        Returns:
            dict: Settings object cleaned.

        """
        return {k: settings[k] for k in DEFAULT_SETTINGS.keys()}

    def update(self, settings):
        """
        Update object attributes from given settings

        Args:
            settings (dict): Dictionnary of settings to update setting
                elements.

        Returns:
            dict: Dictionnary of all current saved settings.

        """
        settings = self.clean(settings)

        self._settings.update(settings)

        for k, v in settings.items():
            setattr(self, k, v)

        return self._settings
