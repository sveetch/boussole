========
Core API
========

Boussole is mainly a commandeline tool but it relies on a core API that may be
used to implement another frontend.

This part of Boussole should not concern end users because they don't directly
exploit it, it documents some behaviors but they should be better documented from Tutorial.

The core API should 100% covered for documentation and unittests.

Modules
*******

.. toctree::
   :maxdepth: 2

   exceptions.rst
   parser.rst
   resolver.rst
   inspector.rst
   finder.rst
   logs.rst
   conf.rst
   compiler.rst
   watcher.rst
