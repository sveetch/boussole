
============
Mind sandbox
============

When CLI is finished and unittests are well done, move every not completed tasks to a github issue.

TODO
****

* [x] Finish API;

  * [x] SCSS parser for import rules;
  * [x] Path resolving through scss project and libraries;
  * [x] Project inspector to find import dependancies;
  * [x] All we need to start building/watching:

    * [x] Resolver and Inspector must follow links for libraries because they will also be watched against changes;
    * [x] When there is more than one file eligible to resolver candidates, Resolver must raise an error about it;
    * [x] Inspector should have method(s) to find all compilable file (aka not partials files) from a given directory (recursively);

  * [x] unittests on API;
  * [x] Documentation coverage on API;

    * [x] Docstring for arguments and module/class descriptions;
    * [x] Renaming unittests test case;
    * [x] Clean every debug pointers;
    * [x] Pass Flake8 validation;

  * [ ] Remove every call to click.echo/secho from API, only return strings and CLI have to print out itself;

* [ ] Settings;

    * [x] Model object, loader, parser, etc..;
    * [ ] Add some settings validations;

* [ ] Commandline interface;

    * [x] Add entry point in setup.py;
    * [x] Configuration file for a project (like the config.rb) with:

          * SOURCES_PATHS: path where to search for files to compile;
          * LIBRARY_PATHS: paths to include as libraries during inspection;
          * TARGET_PATH: Directory where to write all files to compile (preserving their directory structures);

    * [x] Starts cli structure with click;
    * [ ] Be sure compile and watch correctly intercept raised exception from
      boussole (without command interruption and some message in red);
    * [x] 'Compile' command to invoke libsass API to perform compile on files;
    * [x] 'Version' command to display version information;
    * [x] 'Watch' command to start watcher with Watchdog;
    * [ ] 'Check' command to check about a project without compiling (only inspector checking);

* [ ] Usage features;

   * [ ] Usage tutorial for end users;
   * [ ] Improve command line interface informations through colored logging;
   * [ ] Better commandline base long help;
   * [ ] Better short action helps;
   * [ ] Better long action helps;
   * [ ] Before compiling, checksum it, then checksum compiled version then
     display useful short information 'modified', 'identical' (so the user can
     see when it's changes don't change resulting CSS);
   * [ ] See for generating source map;
   * [ ] See to include custom libsass functions;
   * [ ] Color used for output printing should be configurable from a simple
     "init" file alike in user home dir (this must no be part of project
     settings);
