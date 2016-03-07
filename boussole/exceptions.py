# -*- coding: utf-8 -*-
"""
Exceptions
==========

Specific exceptions that Boussole code can raise
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


class UnresolvablePath(BoussoleBaseException):
    """
    Exception to be raised when the resolver can not resolve a given path.
    """
    pass


class CircularImport(BoussoleBaseException):
    """
    Exception to be raised when inspector detect a circular import from
    sources.
    """
    pass
