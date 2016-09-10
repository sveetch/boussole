.. Boussole documentation master file, created by
   sphinx-quickstart on Sun Mar  6 12:12:38 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _SASS: http://sass-lang.com/
.. _LibSass: http://sass-lang.com/libsass
.. _Watchdog: https://github.com/gorakhargosh/watchdog
.. _click: http://click.pocoo.org/5/
.. _libsass-python: https://github.com/dahlia/libsass-python
.. _colorama: https://github.com/tartley/colorama
.. _colorlog: https://github.com/borntyping/python-colorlog
.. _six: https://pythonhosted.org/six/

Welcome to Boussole's documentation!
====================================

Commandline interface to build `SASS`_ projects using `libsass-python`_.

.. Note::
    Old SASS syntax (the *indented syntax*) is not supported.

Features
********

* Stand on `LibSass`_ which is **very fast**;
* **Per project configuration** so you can use it once to compile all of your SASS files from a same project;
* **Simple and useful** command line;
* **Watch mode** for no waste of time during web design integration;
* **Full Python stack**, no Ruby or Node.js stuff needed;
* **Expose a Core API** to use it from Python code;
* Support for **Python2.7** and **Python3.4**;

Links
*****

* Read the documentation on `Read the docs <http://boussole.readthedocs.io/>`_;
* Download its `PyPi package <http://pypi.python.org/pypi/boussole>`_;
* Clone it on its `Github repository <https://github.com/sveetch/boussole>`_;

Dependancies
************

* `six`_;
* `Watchdog`_ == 0.8.3;
* `click`_ == 5.1;
* `libsass-python`_ >= 0.11.0;
* `colorama`_;
* `colorlog`_;

User’s Guide
************

.. toctree::
   :maxdepth: 2

   install.rst
   tutorial.rst
   overview.rst

Developer’s Guide
*****************

.. toctree::
   :maxdepth: 1

   development.rst
   changelog.rst
   api/index.rst

Credits
*******

Logo has been created by **Sébastien Bianco**.