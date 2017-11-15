.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _Sphinx: http://www.sphinx-doc.org
.. _tox: http://tox.readthedocs.io
.. _sphinx-autobuild: https://github.com/GaretJax/sphinx-autobuild

===========
Development
===========

Development requirement
***********************

Boussole is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using `Flake8`_;
* `Sphinx`_ for documentation with enabled `Napoleon`_ extension (using only the *Google style*);

Every requirement is available in file ``requirements/dev.txt``.

Install for development
***********************

First ensure you have `pip`_ and ``python-venv`` package installed then type: ::

    git clone https://github.com/sveetch/boussole.git
    cd boussole
    make install-dev

Boussole will be installed in editable mode from the last commit on master branch.

When it's done, you will be able to check for boussole version, just type: ::

    venv/bin/boussole version

Unittests
---------

Unittests are made to works on `Pytest`_, a shortcut in Makefile is available to start them on your current development install: ::

    make tests


Tox
---

To ease development against multiple Python versions a tox configuration has been added. You are strongly encouraged to use it to test your pull requests.

Before using it you will need to install tox, it is recommended to install it at your system level (tox dependancy is not in tests requirements file): ::

    sudo pip install tox

Then go in the ``boussole`` module directory, where ``the setup.py`` and ``tox.ini`` live and execute tox: ::

    tox

Documentation
-------------

`sphinx-autobuild`_ is installed for a watcher which automatically rebuild HTML documentation when you change sources.

When environnement is activated, you can use following command from ``docs/`` directory: ::

    make livehtml

And go on ``http://127.0.0.1:8002/``.