#!/usr/bin/env python


"""
Testing SumMed Pipeline capabilities 

"""

from multiprocessing import Pipe
import os, pytest, base64, logging, re, json
from time import time
from langcodes import Language
from numpy import extract
from pathlib import Path

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from summed.data import AnalysisConfig, Document, DocumentSource, FileInfo
from summed.pipeline import PipelineFactory
from summed.summed_platform import SumMedPlatform
from summed.user import User, IUser
from summed.space import ISpace, Space
from summed.extractor import Extractor
from summed.analyzer import Analyzer


def test_pipeline_load_english_model(
    platform: SumMedPlatform,
    document_simple_file_en: Document,
):

    document: Document = document_simple_file_en
    pf = PipelineFactory(platform)

    #
    #  English
    #
    nlp: Language = pf.select_pipeline_for_document(document)
    assert nlp.lang == "en"

    # Assert standard pipeline and core summed extensions are present
    assert set(
        [
            "pysbd_sentencizer",
            "tok2vec",
            "tagger",
            "attribute_ruler",
            "lemmatizer",
            "parser",
            "ner",
            "abbreviation_detector",
            "hyponym_detector",
            "biasedtextrank",
            "summed_translation",
            "summed_health_entities",
            "summed_summarizer",
            "summed_gpt3_summarizer",
            "summed_trusted_search",
            "summed_trust_score",
            "summed_glossary_lookup",
            "summed_preprocess_text",
        ]
    ).issubset(nlp.component_names)

    assert nlp.pipe_names == [
        "pysbd_sentencizer",
        "tok2vec",
        "tagger",
        # "parser",
        # "senter",
        "attribute_ruler",
        "lemmatizer",
        "parser",
        "ner",
        "abbreviation_detector",
        "hyponym_detector",
        "biasedtextrank",
        "summed_translation",
        "summed_health_entities",
        "summed_summarizer",
        "summed_gpt3_summarizer",
        "summed_trusted_search",
        "summed_trust_score",
        "summed_glossary_lookup",
        "summed_preprocess_text",
    ]


def test_pipeline_load_german_model(
    platform: SumMedPlatform,
    document_simple_file_de: Document,
):

    document: Document = document_simple_file_de
    pf = PipelineFactory(platform)
    nlp: Language = pf.select_pipeline_for_document(document)
    assert nlp.lang == "de"

    # Assert standard pipeline and core summed extensions are present
    assert set(
        [
            "pysbd_sentencizer",
            "tok2vec",
            "tagger",
            "morphologizer",
            "parser",
            "attribute_ruler",
            "lemmatizer",
            "ner",
            "abbreviation_detector",
            "hyponym_detector",
            "biasedtextrank",
            "summed_translation",
            "summed_health_entities",
            "summed_summarizer",
            "summed_gpt3_summarizer",
            "summed_trusted_search",
            "summed_trust_score",
            "summed_glossary_lookup",
            "summed_preprocess_text",
        ]
    ).issubset(nlp.component_names)

    assert nlp.pipe_names == [
        "pysbd_sentencizer",
        "tok2vec",
        "tagger",
        "morphologizer",
        "parser",
        "attribute_ruler",
        "lemmatizer",
        "ner",
        "abbreviation_detector",
        "hyponym_detector",
        "biasedtextrank",
        "summed_translation",
        "summed_health_entities",
        "summed_summarizer",
        "summed_gpt3_summarizer",
        "summed_trusted_search",
        "summed_trust_score",
        "summed_glossary_lookup",
        "summed_preprocess_text",
    ]


def test_pipeline_load_portuguese_model(
    platform: SumMedPlatform,
    document_simple_file_pt: Document,
):

    document: Document = document_simple_file_pt
    pf = PipelineFactory(platform)
    nlp: Language = pf.select_pipeline_for_document(document)
    assert nlp.lang == "pt"

    # Assert standard pipeline and core summed extensions are present
    assert set(
        [
            "pysbd_sentencizer",
            "tok2vec",
            # "tagger", no pos_tags for portuguese (?)
            "morphologizer",
            "parser",
            "attribute_ruler",
            "lemmatizer",
            "ner",
            "abbreviation_detector",
            "hyponym_detector",
            "biasedtextrank",
            "summed_translation",
            "summed_health_entities",
            "summed_summarizer",
            "summed_gpt3_summarizer",
            "summed_trusted_search",
            "summed_trust_score",
            "summed_glossary_lookup",
            "summed_preprocess_text",
        ]
    ).issubset(nlp.component_names)

    assert nlp.pipe_names == [
        "pysbd_sentencizer",
        "tok2vec",
        # "tagger", no tagger for portuguese
        "morphologizer",
        "parser",
        "attribute_ruler",
        "lemmatizer",
        "ner",
        "abbreviation_detector",
        "hyponym_detector",
        "biasedtextrank",
        "summed_translation",
        "summed_health_entities",
        "summed_summarizer",
        "summed_gpt3_summarizer",
        "summed_trusted_search",
        "summed_trust_score",
        "summed_glossary_lookup",
        "summed_preprocess_text",
    ]


def test_pipeline_load_russian_model(
    platform: SumMedPlatform,
    document_simple_file_ru: Document,
):

    document: Document = document_simple_file_ru
    pf = PipelineFactory(platform)
    nlp: Language = pf.select_pipeline_for_document(document)
    assert nlp.lang == "ru"

    # Assert standard pipeline and core summed extensions are present
    assert set(
        [
            "pysbd_sentencizer",
            "tok2vec",
            # "tagger", no tagger for russian
            "morphologizer",
            "parser",
            "attribute_ruler",
            "lemmatizer",
            "ner",
            "abbreviation_detector",
            "hyponym_detector",
            "biasedtextrank",
            "summed_translation",
            "summed_health_entities",
            "summed_summarizer",
            "summed_gpt3_summarizer",
            "summed_trusted_search",
            "summed_trust_score",
            "summed_glossary_lookup",
            "summed_preprocess_text",
        ]
    ).issubset(nlp.component_names)

    assert nlp.pipe_names == [
        "pysbd_sentencizer",
        "tok2vec",
        # "tagger", no tagger for russian
        "morphologizer",
        "parser",
        "attribute_ruler",
        "lemmatizer",
        "ner",
        "abbreviation_detector",
        "hyponym_detector",
        "biasedtextrank",
        "summed_translation",
        "summed_health_entities",
        "summed_summarizer",
        "summed_gpt3_summarizer",
        "summed_trusted_search",
        "summed_trust_score",
        "summed_glossary_lookup",
        "summed_preprocess_text",
    ]
