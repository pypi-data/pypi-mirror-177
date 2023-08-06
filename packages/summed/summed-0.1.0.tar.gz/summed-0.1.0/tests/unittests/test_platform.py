#!/usr/bin/env python


"""
Testing basic file management functions.
SumMed expects all input files to be in one "space". Users authenticate to their space and can list, upload, replace, and delete files.
The Space is usually backed by Azure Blob Storage, but should be able to be used with other storage options.

"""

import os, pytest, base64, logging, re, json
from typing import Dict, List
from pathlib import Path


from summed.data import DocumentSource, FileInfo, PlatformConfig
from summed.summed_platform import SumMedPlatform
from summed.user import User

from contextlib import contextmanager


@contextmanager
def temp_env(remove: List[str] = [], add: List[Dict[str, str]] = [], **kwargs):
    """
    Creates a temporary environment os.environ, and restores it to original state after the context manager exits.
    """
    _environ = dict(os.environ)
    try:
        for env_to_delete in remove:
            del os.environ[env_to_delete]
        for env_to_add, value in add:
            os.environ[env_to_add] = value

        yield
    finally:
        os.environ.clear()
        os.environ.update(_environ)


def test_start_new_platform():
    platform: SumMedPlatform = SumMedPlatform(PlatformConfig())

    assert platform

    assert platform.config.azure_storage_connection_string
    assert platform.config.azure_storage_container

    assert platform.config.azure_translation_api_key
    assert platform.config.azure_translation_api_endpoint
    assert platform.config.azure_translation_api_location

    storage_container = os.environ["SUMMED_AZURE_STORAGE_CONTAINER"]
    assert storage_container

    # Platform creation should fail, if crucial config is missing
    with temp_env(remove=["SUMMED_AZURE_STORAGE_CONTAINER"]):
        with pytest.raises(Exception):
            platform = SumMedPlatform(config=PlatformConfig())

        # ...but we can manually pass it in (instead of pulling from the environment)
        platform = SumMedPlatform(
            config=PlatformConfig(azure_storage_container=storage_container)
        )
        assert platform

    assert platform
    assert platform.config.azure_storage_container == storage_container


def test_start_platform_active_features():

    platform: SumMedPlatform = SumMedPlatform(PlatformConfig())

    assert platform.has_cognitive_services
    assert platform.has_form_recognizer
    assert platform.has_translator
    assert platform.has_trusted_search
    assert platform.has_text_analytics_for_health
    assert platform.has_dictionary
    assert platform.has_immersive_reader

    # Cognitive services: remove API key, lots of features disappear
    with temp_env(remove=["SUMMED_AZURE_COGNITIVE_SERVICES_API_KEY"]):
        platform = SumMedPlatform(PlatformConfig())
        assert not platform.has_cognitive_services
        assert not platform.has_translator
        assert not platform.has_text_analytics_for_health

        assert platform.has_form_recognizer
        assert platform.has_dictionary
        assert platform.has_trusted_search
        assert platform.has_immersive_reader

    # Removing Form Recognizer: no effect on other features
    with temp_env(remove=["SUMMED_AZURE_FORM_RECOGNIZER_API_KEY"]):
        platform = SumMedPlatform(PlatformConfig())

        assert platform.has_cognitive_services
        assert platform.has_translator
        assert platform.has_text_analytics_for_health
        assert platform.has_dictionary
        assert platform.has_trusted_search
        assert platform.has_immersive_reader

        assert not platform.has_form_recognizer


def test_get_shared_objects_from_platform():
    platform: SumMedPlatform = SumMedPlatform(PlatformConfig())

    assert platform

    assert platform._azure_blob_service_client is None

    # Will return the same object, if called multiple times
    clientA = platform.get_azure_blob_service_client()
    clientB = platform.get_azure_blob_service_client()
    assert clientA == clientB

    # Setting to None, will re-create on next get
    platform._azure_blob_service_client = None
    clientC = platform.get_azure_blob_service_client()
    assert clientA != clientC

    assert platform.get_azure_form_recognizer_client()
    assert platform.get_azure_text_analytics_client()
    # assert platform.get_azure_immersive_reader_token()
    assert platform.get_bing_custom_search_client()
    # assert platform.get_azure_translator_client()
    # assert platform.get_dictionary_client()
    assert platform.configure_spacy_model(model_id="en_core_web_sm")

    assert not platform.configure_spacy_model(model_id="unknown_id")


def test_get_immersive_reader_token():
    platform: SumMedPlatform = SumMedPlatform(PlatformConfig())

    token = platform.get_azure_immersive_reader_token()
    assert token
