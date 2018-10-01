# -*- coding: utf-8 -*-
"""
Exceptions
==========

Specific exceptions that Boussole code can raise.
"""


class BoussoleBaseException(Exception):
    """
    Base for Boussole exceptions.
    """
    pass


class InvalidImportRule(BoussoleBaseException):
    """
    Exception to be raised when the parser encounts an invalid import rule.
    """
    pass


class FinderException(BoussoleBaseException):
    """
    Exception to be raised when error occurs with finder usage.
    """
    pass


class UnresolvablePath(BoussoleBaseException):
    """
    Exception to be raised when the resolver can not resolve a given path.
    """
    pass


class UnclearResolution(BoussoleBaseException):
    """
    Exception to be raised when the resolver encounts multiple existing
    candidates for a path.
    """
    pass


class CircularImport(BoussoleBaseException):
    """
    Exception to be raised when inspector detect a circular import from
    sources.
    """
    pass


class SettingsDiscoveryError(BoussoleBaseException):
    """
    Exception to be raised when config discovery has failed to find settings
    file.
    """
    pass


class SettingsBackendError(BoussoleBaseException):
    """
    Exception to be raised when config loading has failed from a backend.
    """
    pass


class SettingsInvalidError(BoussoleBaseException):
    """
    Exception to be raised when a settings is detected as invalid.
    """
    pass
