# -*- coding: utf-8 -*-
"""
Project configuration
=====================

Todo:
    Some settings containing path should be resolved to current_dir+path if
    they does not starts with /
    
    So we need some rules to filter+patch some settings values.
"""
import os
import copy

from boussole.exceptions import SettingsInvalidError


# Settings manifest define default values and values patchs for each setting
SETTINGS_MANIFEST = {
    'COMPILER_ARGS': {
        'default': [],
        'patchs': [],
    },
    'LIBRARY_PATHS': {
        'default': [],
        'patchs': ['_patch_expand_paths'],
    },
    'SOURCES_PATHS': {
        'default': [],
        'patchs': ['_patch_expand_paths'],
    },
    'TARGET_PATH': {
        'default': None,
        'patchs': ['_patch_expand_path'],
    },
}


# Default values for initial settings object
DEFAULT_SETTINGS = {k: copy.deepcopy(v['default']) for k,v in SETTINGS_MANIFEST.items()}


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

    def filter(self, settings):
        """
        Filter given settings to keep only key names available in
        ``DEFAULT_SETTINGS``.

        Args:
            settings (dict): Loaded settings.

        Returns:
            dict: Settings object filtered.

        """
        return {k: settings[k] for k in DEFAULT_SETTINGS.keys()}

    def patch(self, settings):
        """
        Perform patchs on settings according to their rules in
        ``SETTINGS_MANIFEST``.
        
        Patchs are implemented in their own method that all have the same
        signature:
        
        * Get arguments: initial settings, item name and item value;
        * Return item value possibly patched;

        Args:
            settings (dict): Loaded settings.

        Returns:
            dict: Settings object patched.

        """
        for k,v in settings.items():
            if k in SETTINGS_MANIFEST.items() and SETTINGS_MANIFEST[k].get('patchs', None) is not None:
                pass
        return settings

    def _patch_expand_path(self, settings, name, value):
        """
        Patch a path to expand home directory and make absolute path.
        
        TODO: Not the right behavior. Making absolute path must be done from
              the settings file directory, not from getcwd like
              do "os.path.abspath". Tests will also needs to be rewrited for 
              this. Before everything, move settings file up to
              "tests/datafixtures/".

        Args:
            settings (dict): Initial settings unpatched.
            name (str): Setting name.
            value (str): Path to patch.

        Returns:
            str: Patched path to an absolute path.

        """
        if os.path.isabs(value):
            return value
        
        # Expand home directory if any
        value = os.path.expanduser(value)
        
        # If the path is not yet an absolute directory, make it so
        if not os.path.isabs(value):
            # WARNING: Wrong behavior see TODO
            value = os.path.abspath(value)
        
        return value

    def _patch_expand_paths(self, settings, name, value):
        """
        Apply patch ``_patch_expand_paths`` for each element in list.

        Args:
            settings (dict): Initial settings unpatched.
            name (str): Setting name.
            value (list): List of paths to patch.

        Returns:
            list: Patched path list to an absolute path.

        """
        return [self._patch_expand_path(settings, name, item) for item in value]

    def clean(self, settings):
        """
        Apply filter and patch(s) on given settings.

        Args:
            settings (dict): Loaded settings.

        Returns:
            dict: Settings filter and possibly patched.

        """
        return self.patch(self.filter(settings))

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
