# -*- coding: utf-8 -*-
"""
Backend values patchs
=====================

Patchs are used to modify given settings items like expanding paths. Backends
inherit from ``SettingsPatcher`` to be able to use it in their ``clean()``
method.

Todo:
    * Should be named postprocess.SettingsPostProcessor because it contains
      patchs but will contain some validations soon.
    * Add validation that source_dir is not also set as a library dir (would
      cause some issues in resolving);
"""
import os

from boussole.conf import SETTINGS_MANIFEST


class SettingsPatcher(object):
    """
    Mixin object for all available patch methods to use in
    ``SETTINGS_MANIFEST``.
    """
    projectdir = ''

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
        for k, v in settings.items():
            # Search for patchs method for setting rule
            if k in SETTINGS_MANIFEST and \
               SETTINGS_MANIFEST[k].get('patchs', None) is not None:
                patchs = SETTINGS_MANIFEST[k]['patchs']

                # Apply each patch on value
                for method_name in patchs:
                    settings[k] = getattr(self, method_name)(settings, k, v)

        return settings

    def _patch_expand_path(self, settings, name, value):
        """
        Patch a path to expand home directory and make absolute path.

        Args:
            settings (dict): Initial settings unpatched.
            name (str): Setting name.
            value (str): Path to patch.

        Returns:
            str: Patched path to an absolute path.

        """
        if os.path.isabs(value):
            return os.path.normpath(value)

        # Expand home directory if any
        value = os.path.expanduser(value)

        # If the path is not yet an absolute directory, make it so from base
        # directory if not empty
        if not os.path.isabs(value) and self.projectdir:
            value = os.path.join(self.projectdir, value)

        return os.path.normpath(value)

    def _patch_expand_paths(self, settings, name, value):
        """
        Apply patch ``SettingsPatcher._patch_expand_path`` for each element
        in list.

        Args:
            settings (dict): Initial settings unpatched.
            name (str): Setting name.
            value (list): List of paths to patch.

        Returns:
            list: Patched path list to an absolute path.

        """
        return [self._patch_expand_path(settings, name, item)
                for item in value]
