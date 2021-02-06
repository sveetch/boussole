"""
Unittests
=========

Tests are built for usage with **py.test**.

In data fixtures, not all settings and Sass sources will compile with
libsass. Some of them contains some errors for test needs.

* ``boussole.txt``: Is not an usable settings file, just a dummy file for base
  backend tests;
* ``boussole.json``: Is not an usable settings file, its values are dummy
  pointing to path and files that does not exists;
* ``boussole_polluted.json``: Is almost equivalent of ``boussole_custom.json``
  but polluted with invalid setting names;
* ``boussole_custom.json``: Contain only valid settings, will compile;

For Sass sources, they should all contains a comment when it contains errors.
"""
