# -*- coding: utf-8 -*-
import os
import copy
import pytest

from boussole.conf.post_processor import SettingsPostProcessor


class SettingsPostProcessorTest(SettingsPostProcessor):
    """
    Inherit to add some dummy methods and its own manifest for testing
    processor itself
    """
    settings_manifesto = {
        'field1': {
            'default': [],
            'postprocess': (
                '_dummy_start',
            ),
        },
        'field2': {
            'default': None,
            'postprocess': (
                '_dummy_start',
                '_dummy_end1',
                '_dummy_end2',
            ),
        },
        'field3': {
            'default': [],
            'postprocess': (
                '_dummy_end2',
                '_dummy_end1',
            ),
        },
        'field4': {
            'default': [],
            'postprocess': [],
        },
    }


    def _dummy_start(self, settings, name, value):
        """
        Add 'Hello' at the start of value
        """
        return "Hello {}".format(value)

    def _dummy_end1(self, settings, name, value):
        """
        Add 'world' at the end of value
        """
        return "{} world".format(value)

    def _dummy_end2(self, settings, name, value):
        """
        Add '!' at the end of value
        """
        return "{} !".format(value)


def test_001_dummy_methods(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Just directly test dummy methods"""
    processor = SettingsPostProcessorTest()

    expand_result = processor._dummy_start(sample_project_settings, "DUMMY_NAME", "goodbye")

    assert expand_result == "Hello goodbye"

    expand_result = processor._dummy_end1(sample_project_settings, "DUMMY_NAME", "I rule the")

    assert expand_result == "I rule the world"

    expand_result = processor._dummy_end2(sample_project_settings, "DUMMY_NAME", "Hi")

    assert expand_result == "Hi !"


def test_002_chain_basic(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Testing methods chaining on single rule"""
    processor = SettingsPostProcessorTest()

    expand_result = processor.post_process({
        "field1": "world"
    })

    assert expand_result == {"field1": "Hello world"}


def test_003_chain_more(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Testing methods chaining with many rules"""
    processor = SettingsPostProcessorTest()

    expand_result = processor.post_process({
        "field2": "my"
    })

    assert expand_result == {"field2": "Hello my world !"}


def test_004_chain_order(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Testing methods chaining order is respected"""
    processor = SettingsPostProcessorTest()

    expand_result = processor.post_process({
        "field3": "foo"
    })

    assert expand_result == {"field3": "foo ! world"}


def test_005_chain_empty(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Testing methods chaining with no rules"""
    processor = SettingsPostProcessorTest()

    expand_result = processor.post_process({
        "field4": "foo"
    })

    assert expand_result == {"field4": "foo"}


def test_006_chain_complete(settings, sample_project_settings):
    """conf.post_processor.SettingsPostProcessor: Testing methods chaining on all fields"""
    processor = SettingsPostProcessorTest()

    expand_result = processor.post_process({
        "field1": "world",
        "field2": "my",
        "field3": "foo",
        "field4": "foo",
    })

    assert expand_result == {
        "field1": "Hello world",
        "field2": "Hello my world !",
        "field3": "foo ! world",
        "field4": "foo",
    }
