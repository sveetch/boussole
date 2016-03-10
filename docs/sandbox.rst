
============
Mind sandbox
============


TODO
****

* [ ] Finish API;

  * [x] SCSS parser for import rules;
  * [x] Path resolving through scss project and libraries;
  * [x] Project inspector to find import dependancies;
  * [ ] All we need to start building/watching:
  
    * [x] Resolver and Inspector must follow links for libraries because they will also be watched against changes;
    * [x] When there is more than one file eligible to resolver candidates, Resolver must raise an error about it;
    * [ ] Inspector should have method(s) to find all compilable file (aka not partials files) from a given directory (recursively);
    
  * [x] unittests on API;
  * [x] Documentation coverage on API;
  
    * [x] Docstring for arguments and module/class descriptions;
    * [x] Renaming unittests test case;
    * [x] Clean every debug pointers;
    * [x] Pass Flake8 validation;

* [ ] Commandline interface;

    * [x] Add entry point in setup.py;
    * [ ] Configuration file for a project (like the config.rb) with:
        
          * SOURCES_PATHS: paths where to search for files to compile;
          * LIBRARY_PATHS: paths to include as libraries during inspection;
          * TARGET_PATH: Directory where to write all files to compile (preserving their directory structures);
          * COMPILER_ARGS: list/map of arguments to pass to the compiler;
    
    * [ ] Starts cli structure with click;
    * [ ] 'Build' command to invoke libsass API to perform compile on files;
    * [ ] 'Watch' command to start watcher with Watchdog;
    * [ ] 'Check' command to check about a project without compile (only inspector checking);
