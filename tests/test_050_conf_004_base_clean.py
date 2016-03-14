# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.base_backend import SettingsLoaderBase


#def test_settings_base_clean_001(settings, sample_project_settings):
    #"""conf.base_backendSettingsLoaderBase: Ensure cleaning dont drop anything"""
    #settings_loader = SettingsLoaderBase()
    
    #assert settings_loader.clean(sample_project_settings) == sample_project_settings


#def test_settings_base_clean_002(settings, sample_project_settings):
    #"""conf.base_backendSettingsLoaderBase: Ensure return elements match the enabled name elements"""
    #settings_loader = SettingsLoaderBase()
    
    #cleaned = settings_loader.clean(sample_project_settings)
    ## Sort lists keys to ensure they will be in same order
    #cleaned_names = sorted(cleaned.keys())
    #enabled_names = sorted(settings_loader._enabled_names)
    
    #assert cleaned_names == enabled_names


#def test_settings_base_clean_003(settings, sample_project_settings):
    #"""conf.base_backendSettingsLoaderBase: Clean extra elements"""
    #settings_loader = SettingsLoaderBase()
    
    #fake_settings = copy.deepcopy(sample_project_settings)
    #fake_settings.update({
        #'foo': True,
        #'bar': 42,
        #'plonk': [],
    #})
    
    #assert settings_loader.clean(fake_settings) == sample_project_settings
