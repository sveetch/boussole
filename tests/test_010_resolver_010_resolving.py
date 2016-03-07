# -*- coding: utf-8 -*-
import os
import pytest

from boussole.exceptions import UnresolvablePath

def test_resolver_resolve_basic(settings, parser, resolver):
    """resolver.ImportPathsResolver: Resolve paths from basic sample"""
    sourcepath = os.path.join(settings.sample_path, 'main_basic.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())
        
    resolved_paths = resolver.resolve(sourcepath, finded_paths)
    
    assert resolved_paths == [
        os.path.join(settings.sample_path, '_vendor.scss'),
        os.path.join(settings.sample_path, '_empty.scss'),
    ]


def test_resolver_resolve_library(settings, parser, resolver):
    """resolver.ImportPathsResolver: Resolve paths from main_using_libs.scss 
    that use included libraries"""
    sourcepath = os.path.join(settings.sample_path, 'main_using_libs.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())
    
    resolved_paths = resolver.resolve(
        sourcepath, 
        finded_paths, 
        library_paths=settings.libraries_fixture_paths
    )
    
    assert resolved_paths == [
        os.path.join(settings.lib2_path, 'addons/_some_addon.scss'),
        os.path.join(settings.sample_path, 'main_basic.scss'),
        os.path.join(settings.sample_path, 'components/_webfont.scss'),
        os.path.join(settings.lib1_path, 'library_1_fullstack.scss'),
    ]


def test_resolver_resolve_commented(settings, parser, resolver):
    """resolver.ImportPathsResolver: Resolve paths from sample with comments"""
    sourcepath = os.path.join(settings.sample_path, 'main_commented.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())
    
    resolved_paths = resolver.resolve(sourcepath, finded_paths)
    
    assert resolved_paths == [
        os.path.join(settings.sample_path, '_vendor.scss'),
        os.path.join(settings.sample_path, 'components/_filename_test_1.scss'),
        os.path.join(settings.sample_path, '_empty.scss'),
    ]


def test_resolver_resolve_error(settings, parser, resolver):
    """resolver.ImportPathsResolver: Exception on wrong import path"""
    sourcepath = os.path.join(settings.sample_path, 'main_error.scss')
    with open(sourcepath) as fp:
        finded_paths = parser.parse(fp.read())
        
    with pytest.raises(UnresolvablePath):
        resolver.resolve(
            sourcepath, 
            finded_paths, 
            library_paths=settings.libraries_fixture_paths
        )
