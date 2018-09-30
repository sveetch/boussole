"""
Project management
==================
"""
import os

from boussole.exceptions import SettingsInvalidError, SettingsBackendError
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml


class ProjectBase(object):
    """
    Project base

    Arguments:
        backend_name (string): Backend name, can be either ``json`` or
            ``yaml``.

    Attributes:
        _engines: Available Configuration backends. Read only.
        backend_name: Backend name to use from available ones.
        backend_engine: Backend engine selected from given name.
    """
    _engines = {
        'json': SettingsBackendJson,
        'yaml': SettingsBackendYaml,
    }

    def __init__(self, backend_name, **kwargs):
        self.backend_name = backend_name
        self.backend_engine = self.get_backend_engine(self.backend_name,
                                                      **kwargs)

    def get_backend_engine(self, name, **kwargs):
        """
        Get backend engine from given name.

        Args:
            (string): Path to validate.

        Raises:
            boussole.exceptions.SettingsBackendError: If given backend name
                does not match any available engine.

        Returns:
            object: Instance of selected backend engine.
        """
        if name not in self._engines:
            msg = "Given settings backend is unknowed: {}"
            raise SettingsBackendError(msg.format(name))

        return self._engines[name](**kwargs)


class ProjectStarter(ProjectBase):
    """
    Provide methods to create a new Sass Project
    """
    def valid_paths(self, *args):
        """
        Validate that given paths are not the same.

        Args:
            (string): Path to validate.

        Raises:
            boussole.exceptions.SettingsInvalidError: If there is more than one
                occurence of the same path.

        Returns:
            bool: ``True`` if paths are validated.
        """
        for i, path in enumerate(args, start=0):
            cp = list(args)
            current = cp.pop(i)
            if current in cp:
                raise SettingsInvalidError("Multiple occurences finded for "
                                           "path: {}".format(current))

        return True

    def expand(self, basedir, config, sourcedir, targetdir, cwd):
        """
        Validate that given paths are not the same.

        Args:
            basedir (string): Project base directory used to prepend relative
                paths. If empty or equal to '.', it will be filled with current
                directory path.
            config (string): Settings file path.
            sourcedir (string): Source directory path.
            targetdir (string): Compiled files target directory path.
            cwd (string): Current directory path to prepend base dir if empty.

        Returns:
            tuple: Expanded arguments in the same order
        """

        # Expand home directory if any
        expanded_basedir = os.path.expanduser(basedir)
        expanded_config = os.path.expanduser(config)
        expanded_sourcedir = os.path.expanduser(sourcedir)
        expanded_targetdir = os.path.expanduser(targetdir)

        # If not absolute, base dir is prepended with current directory
        if not os.path.isabs(expanded_basedir):
            expanded_basedir = os.path.join(cwd, expanded_basedir)
        # Prepend paths with base dir if they are not allready absolute
        if not os.path.isabs(expanded_config):
            expanded_config = os.path.join(expanded_basedir,
                                           expanded_config)
        if not os.path.isabs(expanded_sourcedir):
            expanded_sourcedir = os.path.join(expanded_basedir,
                                              expanded_sourcedir)
        if not os.path.isabs(expanded_targetdir):
            expanded_targetdir = os.path.join(expanded_basedir,
                                              expanded_targetdir)

        # Normalize paths
        expanded_basedir = os.path.normpath(expanded_basedir)
        expanded_config = os.path.normpath(expanded_config)
        expanded_sourcedir = os.path.normpath(expanded_sourcedir)
        expanded_targetdir = os.path.normpath(expanded_targetdir)

        return (expanded_basedir, expanded_config, expanded_sourcedir,
                expanded_targetdir)

    def commit(self, sourcedir, targetdir, abs_config, abs_sourcedir,
               abs_targetdir):
        """
        Commit project structure and configuration file

        Args:
            sourcedir (string): Source directory path.
            targetdir (string): Compiled files target directory path.
            abs_config (string): Configuration file absolute path.
            abs_sourcedir (string): ``sourcedir`` expanded as absolute path.
            abs_targetdir (string): ``targetdir`` expanded as absolute path.
        """
        config_path, config_filename = os.path.split(abs_config)

        if not os.path.exists(config_path):
            os.makedirs(config_path)
        if not os.path.exists(abs_sourcedir):
            os.makedirs(abs_sourcedir)
        if not os.path.exists(abs_targetdir):
            os.makedirs(abs_targetdir)

        # Dump settings file
        self.backend_engine.dump({
            'SOURCES_PATH': sourcedir,
            'TARGET_PATH': targetdir,
            "LIBRARY_PATHS": [],
            "OUTPUT_STYLES": "nested",
            "SOURCE_COMMENTS": False,
            "EXCLUDES": []
        }, abs_config, indent=4)

    def init(self, basedir, config, sourcedir, targetdir, cwd='', commit=True):
        """
        Init project structure and configuration from given arguments

        Args:
            basedir (string): Project base directory used to prepend relative
                paths. If empty or equal to '.', it will be filled with current
                directory path.
            config (string): Settings file path.
            sourcedir (string): Source directory path.
            targetdir (string): Compiled files target directory path.

        Keyword Arguments:
            cwd (string): Current directory path to prepend base dir if empty.
            commit (bool): If ``False``, directory structure and settings file
                won't be created.

        Returns:
            dict: A dict containing expanded given paths.
        """
        if not basedir:
            basedir = '.'

        # Expand home directory if any
        abs_basedir, abs_config, abs_sourcedir, abs_targetdir = self.expand(
            basedir, config,
            sourcedir, targetdir,
            cwd
        )

        # Valid every paths are ok
        self.valid_paths(abs_config, abs_sourcedir, abs_targetdir)

        # Create required directory structure
        if commit:
            self.commit(sourcedir, targetdir, abs_config, abs_sourcedir,
                        abs_targetdir)

        return {
            'basedir': abs_basedir,
            'config': abs_config,
            'sourcedir': abs_sourcedir,
            'targetdir': abs_targetdir,
        }
