# -*- coding: utf-8 -*-
"""
Backend discover
================

"""
import os
from collections import OrderedDict

from boussole.exceptions import SettingsDiscoveryError


class Discover:
    """
    Should be able to find a settings file without any specific backend given,
    just a directory path (the base dir) is required.

    So:

    * If a file name is explicitely given, use it to find backend;
    * If no file name is given but a backend is, use its default file name;
    * If file name nor backend is given, start full discover process:

        * Get all backend default settings file name;
        * Search for any of these available settings file names;
        * If no available settings file name if finded, discovering fail;
        * If one file name is given assume backend from file name;

    backends (list): List of backend engines to get available backend engines.
    """

    def __init__(self, backends=[]):
        self.backends = backends

        indexes = self.scan_backends(self.backends)
        self.engines, self.filenames, self.extensions = indexes

    def scan_backends(self, backends):
        """
        From given backends create and return engine, filename and extension
        indexes.

        Arguments:
            backends (list): List of backend engines to scan. Order does matter
                since resulted indexes are stored in an ``OrderedDict``. So
                discovering will stop its job if it meets the first item.

        Returns:
            tuple: Engine, filename and extension indexes where:

            * Engines are indexed on their kind name with their backend object
              as value;
            * Filenames are indexed on their filename with engine kind name as
              value;
            * Extensions are indexed on their extension with engine kind name
              as value;
        """
        engines = OrderedDict()
        filenames = OrderedDict()
        extensions = OrderedDict()

        for item in backends:
            engines[item._kind_name] = item
            filenames[item._default_filename] = item._kind_name
            extensions[item._file_extension] = item._kind_name

        return engines, filenames, extensions

    def get_engine(self, filepath, kind=None):
        """
        From given filepath try to discover which backend format to use.

        Discovering is pretty naive as it find format from file extension.

        Args:
            filepath (str): Settings filepath or filename.

        Keyword Arguments:
            kind (str): A format name to enforce a specific backend. Can be any
                value from attribute ``_kind_name`` of available backend
                engines.

        Raises:
            boussole.exceptions.SettingsDiscoveryError: If extension is
            unknowed or if given format name is unknowed.

        Returns:
            object: Backend engine class.

        """
        if not kind:
            extension = os.path.splitext(filepath)[1]
            if not extension:
                msg = ("Unable to discover settings format from an empty file "
                       "extension: {}")
                raise SettingsDiscoveryError(msg.format(filepath))
            elif extension[1:] not in self.extensions:
                msg = ("Settings file extension is unknowed from available "
                       "backends: {}")
                raise SettingsDiscoveryError(msg.format(filepath))
            kind = self.extensions[extension[1:]]
        elif kind not in self.engines:
            msg = "Given settings format is unknow: {}"
            raise SettingsDiscoveryError(msg.format(kind))

        return self.engines[kind]

    def guess_filename(self, basedir, kind=None):
        """
        Try to find existing settings filename from base directory using
        default filename from available engines.

        First finded filename from available engines win. So registred engines
        order matter.

        Arguments:
            basedir (string): Directory path where to search for.

        Keyword Arguments:
            kind (string): Backend engine kind name to search for default
                settings filename. If not given, search will be made for
                default settings filename from all available backend engines.

        Returns:
            tuple: Absolute filepath and backend engine class.
        """
        if kind:
            filepath = os.path.join(basedir,
                                    self.engines[kind]._default_filename)
            if os.path.exists(filepath):
                return filepath, self.engines[kind]

        for filename, kind in self.filenames.items():
            filepath = os.path.join(basedir, filename)
            if os.path.exists(filepath):
                return filepath, self.engines[kind]

        msg = "Unable to find any settings in directory: {}"
        raise SettingsDiscoveryError(msg.format(basedir))

    def search(self, filepath=None, basedir=None, kind=None):
        """
        Search for a settings file.

        Keyword Arguments:
            filepath (string): Path to a config file, either absolute or
                relative. If absolute set its directory as basedir (omitting
                given basedir argument). If relative join it to basedir.
            basedir (string): Directory path where to search for.
            kind (string): Backend engine kind name (value of attribute
                ``_kind_name``) to help discovering with empty or relative
                filepath. Also if explicit absolute filepath is given, this
                will enforce the backend engine (such as yaml kind will be
                forced for a ``foo.json`` file).

        Returns:
            tuple: Absolute filepath and backend engine class.
        """
        # None values would cause trouble with path joining
        if filepath is None:
            filepath = ''
        if basedir is None:
            basedir = '.'

        if not basedir and not filepath:
            msg = "Either basedir or filepath is required for discovering"
            raise SettingsDiscoveryError(msg)

        if kind and kind not in self.engines:
            msg = "Given settings format is unknow: {}"
            raise SettingsDiscoveryError(msg.format(kind))

        # Implicit filename to find from backend
        if not filepath:
            filename, engine = self.guess_filename(basedir, kind)
            filepath = os.path.join(basedir, filename)
        # Explicit filename dont have to search for default backend file and
        # blindly force given backend if any
        else:
            if os.path.isabs(filepath):
                basedir, filename = os.path.split(filepath)
            else:
                filepath = os.path.join(basedir, filepath)

            if not os.path.exists(filepath):
                msg = "Given settings file does not exists: {}"
                raise SettingsDiscoveryError(msg.format(filepath))

            engine = self.get_engine(filepath, kind)

        return filepath, engine
