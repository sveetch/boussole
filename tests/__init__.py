"""
Unittests
=========

Tests are builded using **py.test**.

In data fixtures, not all settings and SASS stylesheets will compile with
libsass. Some of them contains some errors for test needs.

* ``settings.txt``: Is not an usable settings file, just a dummy file for base backend tests;
* ``settings.json``: Is not an usable settings file, its values are dummy pointing to path and files that does not exists;
* ``settings_polluted.json``: Is almost equivalent of ``settings_custom.json`` but polluted with invalid setting names;
* ``settings_custom.json``: Contain only valid settings, will compile;

For SASS stylesheets, they should all contains a comment when it contains errors.
"""