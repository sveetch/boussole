# -*- coding: utf-8 -*-
"""
Settings model
==============

"""
from boussole.conf import DEFAULT_SETTINGS


class Settings(object):
    """
    Settings model object

    Class init method fills object attributes from either given initial
    settings (if given) or default ones from ``DEFAULT_SETTINGS``.

    Keyword Arguments:
        initial (dict): A dictionnary of settings for initial values.
    """
    def __init__(self, initial=None):
        self._settings = {}
        self.update(initial or DEFAULT_SETTINGS)

    def clean(self, settings):
        """
        Filter given settings to keep only key names available in
        ``DEFAULT_SETTINGS``.

        Args:
            settings (dict): Loaded settings.

        Returns:
            dict: Settings object filtered.

        """
        return {k: v for k, v in settings.items() if k in DEFAULT_SETTINGS}

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

        # Update internal dict
        self._settings.update(settings)

        # Push every setting items as class object attributes
        for k, v in settings.items():
            setattr(self, k, v)

        return self._settings
