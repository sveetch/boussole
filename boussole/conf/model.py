# -*- coding: utf-8 -*-
"""
Settings model
==============

This define the model object containing settings that will be passed to
interfaces.

"""
import copy

from boussole.conf import SETTINGS_MANIFEST


# Default values for initial settings object
DEFAULT_SETTINGS = {k: copy.deepcopy(v['default'])
                    for k, v in SETTINGS_MANIFEST.items()}


class Settings(object):
    """
    Settings model object

    Class init method fills object attributes from default settings
    (``DEFAULT_SETTINGS``) then update it with initial settings if given.

    Settings are available as object attributes, there is also a private
    ``_settings`` attribute containing a dict of all stored settings. You are
    strongly advised to never directly manipulate the ``_settings`` attribute.
    Instead, allways use the ``update()`` method.

    Note:
        Model is only about data model, there is no other validation that
        available 'fields' from ``DEFAULT_SETTINGS``.

        If you intend to manually open and fill a Settings instance, remember
        to allways use absolute paths in your settings. Relative path will
        cause issues in resolving that lead to wrong compilations.

        You may also apply post processor validation to ensure your datas.

    Keyword Arguments:
        initial (dict): A dictionnary of settings for initial values.
    """
    def __init__(self, initial={}):
        self._settings = copy.deepcopy(DEFAULT_SETTINGS)
        if initial:
            initial = self.clean(initial)
            self._settings.update(initial)
        self.set_settings(self._settings)

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

    def set_settings(self, settings):
        """
        Set every given settings as object attributes.

        Args:
            settings (dict): Dictionnary of settings.

        """
        for k, v in settings.items():
            setattr(self, k, v)

    def update(self, settings):
        """
        Update object attributes from given settings

        Args:
            settings (dict): Dictionnary of elements to update settings.

        Returns:
            dict: Dictionnary of all current saved settings.

        """
        settings = self.clean(settings)

        # Update internal dict
        self._settings.update(settings)

        # Push every setting items as class object attributes
        self.set_settings(settings)

        return self._settings
