"""
Some fixture methods
"""
import os
import pytest

import boussole

from boussole.parser import ScssImportsParser
from boussole.finder import ScssFinder
from boussole.resolver import ImportPathsResolver
from boussole.inspector import ScssInspector
from boussole.compiler import SassCompileHelper
from boussole.project import ProjectStarter


class FixturesSettingsTestMixin(object):
    """Mixin containing some basic settings"""
    def __init__(self):
        # Base fixture datas directory
        self.tests_dir = 'tests'
        self.tests_path = os.path.normpath(
            os.path.join(
                os.path.abspath(os.path.dirname(boussole.__file__)),
                '..',
                self.tests_dir,
            )
        )
        self.fixtures_dir = 'data_fixtures'
        self.fixtures_path = os.path.join(
            self.tests_path,
            self.fixtures_dir
        )

        # Sample project
        self.sample_dir = "sample_project"
        self.sample_path = os.path.join(self.fixtures_path, self.sample_dir)

        # Some sample libraries
        self.lib1_dir = 'library_1'
        self.lib2_dir = 'library_2'
        self.lib1_path = os.path.join(self.fixtures_path, self.lib1_dir)
        self.lib2_path = os.path.join(self.fixtures_path, self.lib2_dir)
        self.libraries_fixture_paths = [
            self.lib1_path,
            self.lib2_path,
        ]


@pytest.fixture(scope='session')
def temp_builds_dir(tmpdir_factory):
    """Prepare a temporary build directory"""
    fn = tmpdir_factory.mktemp('builds')
    return fn


@pytest.fixture(scope="module")
def settings():
    """Initialize and return settings (mostly paths) for fixtures (scope at module level)"""
    return FixturesSettingsTestMixin()


@pytest.fixture(scope="module")
def parser():
    """Initialize and return SCSS parser (scope at module level)"""
    return ScssImportsParser()


@pytest.fixture(scope="module")
def resolver():
    """Initialize and return Path resolver (scope at module level)"""
    return ImportPathsResolver()


@pytest.fixture(scope="function")
def inspector():
    """Initialize and return SCSS inspector (scope at function level)"""
    return ScssInspector()


@pytest.fixture(scope="module")
def finder():
    """Initialize and return SCSS finder (scope at module level)"""
    return ScssFinder()


@pytest.fixture(scope="module")
def compiler():
    """Initialize and return SCSS compile helper (scope at module level)"""
    return SassCompileHelper()


@pytest.fixture(scope="module")
def projectstarter():
    """Initialize and return Project starter (scope at module level)"""
    return ProjectStarter()


@pytest.fixture(scope="module")
def sample_project_settings():
    """Return sample settings dictionnary with expected values (scope at
       module level).

       Warning, this will raise exception from everything involving
       'Backend.clean()' because every paths does not exists"""
    return {
        #'COMPILER_ARGS': [],
        'LIBRARY_PATHS': [
            u'/home/lib1',
            u'/home/lib2',
        ],
        'SOURCES_PATH': u'/home/foo',
        'TARGET_PATH': u'/home/bar',
        'OUTPUT_STYLES': u'nested',
        'SOURCE_COMMENTS': False,
        'SOURCE_MAP': False,
        "EXCLUDES": [],
    }


@pytest.fixture(scope="module")
def custom_project_settings():
    """Return custom settings dictionnary with expected values (scope at
       module level)"""
    fixtures_settings = FixturesSettingsTestMixin()
    return {
        'LIBRARY_PATHS': [
            os.path.join(fixtures_settings.fixtures_path, u'library_1'),
            os.path.join(fixtures_settings.fixtures_path, u'library_2'),
        ],
        'SOURCES_PATH': os.path.join(fixtures_settings.fixtures_path, u'sample_project'),
        'TARGET_PATH': fixtures_settings.fixtures_path,
        'OUTPUT_STYLES': u'expanded',
        'SOURCE_COMMENTS': True,
        'SOURCE_MAP': False,
        "EXCLUDES": [
            "main_error.scss",
            "main_circular_5.scss",
            "main_circular_0.scss",
            "main_circular_4.scss",
            "main_circular_3.scss",
            "main_circular_1.scss",
            "main_circular_2.scss",
            "main_circular_bridge.scss",
            "main_twins_*.scss",
            "*/twin_*.scss"
        ],
    }
