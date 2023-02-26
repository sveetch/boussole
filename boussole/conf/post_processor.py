# -*- coding: utf-8 -*-
"""
Settings backend post processing
================================

Post processing methods are used to modify or validate given settings items.

Base backend inherit from ``SettingsPostProcessor`` to be able to use it in
its ``clean()`` method.
"""
import os
import datetime
from hashlib import blake2b
from uuid import uuid4

from ..exceptions import SettingsInvalidError

from . import SETTINGS_MANIFEST


class SettingsPostProcessor(object):
    """
    Mixin object for all available post processing methods to use in
    settings manifest (default manifest comes from ``SETTINGS_MANIFEST``).
    """
    settings_manifesto = SETTINGS_MANIFEST
    projectdir = ""

    def post_process(self, settings):
        """
        Perform post processing methods on settings according to their
        definition in manifest.

        Post process methods are implemented in their own method that have the
        same signature:

        * Get arguments: Current settings, item name and item value;
        * Return item value possibly patched;

        Args:
            settings (dict): Loaded settings.

        Returns:
            dict: Settings object possibly modified (depending from applied
            post processing).

        """
        for k in settings:
            # Search for post process rules for setting in manifest
            if (
                k in self.settings_manifesto and
                self.settings_manifesto[k].get("postprocess", None) is not None
            ):
                rules = self.settings_manifesto[k]["postprocess"]

                # Chain post process rules from each setting
                for method_name in rules:
                    settings[k] = getattr(self, method_name)(
                        settings,
                        k,
                        settings[k]
                    )

        return settings

    def _patch_expand_path(self, settings, name, value):
        """
        Patch a path to expand home directory and make absolute path.

        Args:
            settings (dict): Current settings.
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
        Apply ``SettingsPostProcessor._patch_expand_path`` to each element in
        list.

        Args:
            settings (dict): Current settings.
            name (str): Setting name.
            value (list): List of paths to patch.

        Returns:
            list: Patched path list to an absolute path.

        """
        return [self._patch_expand_path(settings, name, item)
                for item in value]

    def _validate_path(self, settings, name, value):
        """
        Validate path exists

        Args:
            settings (dict): Current settings.
            name (str): Setting name.
            value (str): Path to validate.

        Raises:
            boussole.exceptions.SettingsInvalidError: If path does not exists.

        Returns:
            str: Validated path.

        """
        if not os.path.exists(value):
            msg = "Path from setting '{name}' does not exists: {value}"
            raise SettingsInvalidError(msg.format(name=name, value=value))

        return value

    def _validate_paths(self, settings, name, value):
        """
        Apply ``SettingsPostProcessor._validate_path`` to each element in
        list.

        Args:
            settings (dict): Current settings.
            name (str): Setting name.
            value (list): List of paths to patch.

        Raises:
            boussole.exceptions.SettingsInvalidError: Once a path does not
                exists.

        Returns:
            list: Validated paths.

        """
        return [self._validate_path(settings, name, item)
                for item in value]

    def _validate_required(self, settings, name, value):
        """
        Validate a required setting (value can not be empty)

        Args:
            settings (dict): Current settings.
            name (str): Setting name.
            value (str): Required value to validate.

        Raises:
            boussole.exceptions.SettingsInvalidError: If value is empty.

        Returns:
            str: Validated value.

        """
        if not value:
            msg = "Required value from setting '{name}' must not be empty."
            raise SettingsInvalidError(msg.format(name=name))

        return value

    def _patch_hash_suffix(self, settings, name, value):
        """
        Coerce setting ``HASH_SUFFIX`` to the right value.

        Args:
            settings (dict): Current settings.
            name (str): Setting name.
            value (str): Required value to patch.

        Returns:
            object: It may be:

            * None if value is an empty string, None or False;
            * If value is ``:blake2``, this will return a hash from black2b with a
              length of 20 characters (almost guaranteed to be unique);
            * If value is ``:blake2``, this will return a hash from uuid4 with a
              length of 32 characters (guaranteed to be unique);
            * If True, assume it enables the default hash engine which is ``:blake2``;
            * A string if value is a string that do not match any hash engine name;

        """
        if not value:
            return None

        if value is True or value == ":blake2":
            # Use the current datetime with microseconds to build the hash
            value = blake2b(
                datetime.datetime.now().isoformat().encode('utf-8'),
                digest_size=10
            ).hexdigest()
        elif value == ":uuid":
            # UUID is unique ID that does not need any content, we just remove dashes
            # for shorter string
            value = str(uuid4()).replace("-", "")

        return value
