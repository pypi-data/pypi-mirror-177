#!/usr/bin/env python


"""
Testing basic translation features 

"""

import os, pytest, base64, logging, re, json
from pathlib import Path


from summed.data import DocumentSource, FileInfo
from summed.summed_platform import SumMedPlatform
from summed.user import User
from summed.space import ISpace, Space

from summed.translation import AzureTranslator
from summed.detector import Detector

import dotenv

dotenv.load_dotenv()


def test_detect_language(platform: SumMedPlatform):
    detector = Detector(platform)
    assert detector.detect_language("111") == "en"
    assert detector.detect_language("text111") == "en"
    assert detector.detect_language("пф111") != "en"
    assert detector.detect_language("Привет мой мир") == "ru"
    assert detector.detect_language("Hello my world") == "en"
    assert detector.detect_language("Hallo meine Welt!") == "de"
    assert detector.detect_language("a a a") == "en"


@pytest.mark.needs_internet
def test_translate_english_to_english(platform: SumMedPlatform):
    assert platform.config.azure_translation_api_key
    assert platform.config.azure_translation_api_endpoint
    assert platform.config.azure_translation_api_location

    translator = AzureTranslator(platform)
    # This translation should fail because the language for translation is incorrect
    # Exception handled successfully
    # assert translator.translate("hello world", "eeen") == "hello world"
    assert translator.translate("hello my world", "en") == "hello my world"
    # assert translator.translate("hello my world", "ru") == "Привет мой мир"


@pytest.mark.needs_internet
def test_translate_russian_to_english(platform: SumMedPlatform):
    translator = AzureTranslator(platform)
    assert translator.translate("Привет мой мир", "en") == "Hello my world"


@pytest.mark.needs_internet
def test_translate_english_to_german(platform: SumMedPlatform):
    translator = AzureTranslator(platform)
    assert translator.translate("hello my world", "de") == "Hallo meine Welt"
