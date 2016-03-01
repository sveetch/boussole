# -*- coding: utf-8 -*-
import os
import pytest


def test_010_check_candidate_ok1(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates correct case 1"""
    candidates = resolver.candidate_paths("vendor")
    assert resolver.check_candidate_exists(settings.sample_path, candidates) == os.path.join(settings.sample_path, "_vendor.scss")

def test_011_check_candidate_ok2(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates correct case 2"""
    candidates = resolver.candidate_paths("components/_filename_test_2")
    assert resolver.check_candidate_exists(settings.sample_path, candidates) == os.path.join(settings.sample_path, "components/_filename_test_2.scss")

def test_012_check_candidate_ok3(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates correct case 3"""
    candidates = resolver.candidate_paths("components/filename_test_6.plop.scss")
    assert resolver.check_candidate_exists(settings.sample_path, candidates) == os.path.join(settings.sample_path, "components/_filename_test_6.plop.scss")

def test_013_check_candidate_ok4(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates correct case 4"""
    basepath = os.path.join(settings.sample_path, "components")
    candidates = resolver.candidate_paths("webfont")
    assert resolver.check_candidate_exists(basepath, candidates) == os.path.join(basepath, "_webfont.scss")

def test_014_check_candidate_ok5(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates correct case 5"""
    basepath = os.path.join(settings.sample_path, "components")
    candidates = resolver.candidate_paths("../components/webfont_icons")
    assert resolver.check_candidate_exists(basepath, candidates) == os.path.join(basepath, "../components/_webfont_icons.scss")

def test_015_check_candidate_wrong1(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates wrong case 1"""
    candidates = resolver.candidate_paths("dont_exists")
    assert resolver.check_candidate_exists(settings.sample_path, candidates) == False

def test_016_check_candidate_wrong2(settings, parser, resolver):
    """resolver.ImportPathsResolver: Check candidates wrong case 2"""
    candidates = resolver.candidate_paths("css_filetest.sass")
    assert resolver.check_candidate_exists(settings.sample_path, candidates) == False
