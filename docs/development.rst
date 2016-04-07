.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org

===========
Development
===========

Development requirement
***********************

Boussole is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using ``flake8``;
* ``Sphinx`` for documentation with enabled `Napoleon`_ extension (using only the *Google style*);

Every requirement is available in file ``dev_requirements.txt``.

Install for development
***********************

First ensure you have `pip`_ and `virtualenv`_ installed, then in your console terminal type this: ::

    mkdir boussole-dev
    cd boussole-dev
    virtualenv --system-site-packages .
    source bin/activate
    pip install -r https://raw.githubusercontent.com/sveetch/boussole/master/dev_requirements.txt

Boussole will be installed in editable mode from the last commit on master branch.

When pip has finished installing requirements with success, you will be able to check for boussole version, just type: ::

    boussole version
