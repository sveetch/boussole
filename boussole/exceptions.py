# -*- coding: utf-8 -*-
"""
Specific Boussole exceptions
"""
class BoussoleException(Exception):
    pass

class InvalidImportRule(BoussoleException):
    pass

class CircularImport(BoussoleException):
    pass
