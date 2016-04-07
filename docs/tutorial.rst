.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org

========
Tutorial
========

Once Boussole is correctly installed, you will be able to start a project to work on.

#. Go within your new SASS project and write a ``settings.json`` file with following content:

    .. sourcecode:: json

        {
            "SOURCES_PATH": "scss",
            "LIBRARY_PATHS": [],
            "TARGET_PATH": "css",
        }
#. Create directory ``scss``;
#. Write some SASS file into ``scss`` directory;
#. From your SASS project directory (where belong the ``settings.json`` file) just execute command: ::

    boussole compile
#. And voila, your SASS files (if valid) should have been compiled to the ``css`` directory;
