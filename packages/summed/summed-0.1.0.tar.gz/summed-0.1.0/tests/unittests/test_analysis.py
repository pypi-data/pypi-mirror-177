#!/usr/bin/env python


"""
Testing SumMed Analysis features 

"""

import os, pytest, base64, logging, re, json
from pydoc import doc
from pyparsing import original_text_for
from this import d
from pathlib import Path
from summed.pipeline import PipelineFactory

from summed.data import (
    AnalysisConfig,
    Document,
    DocumentSource,
    FileInfo,
    TermExplanation,
)
from summed.summed_platform import SumMedPlatform
from summed.space import ISpace, Space
from summed.extractor import Extractor
from summed.analyzer import Analyzer
from summed.detector import Detector
from summed.pipeline import PipelineFactory
from summed.analysis.configurations import (
    CALCULATE_TRUST_SCORE,
    CREATE_ABSTRACTIVE_SUMMARY,
    CREATE_SUMMARY,
    DETECT_ENTITIES,
    DETECT_HEALTH_ENTITIES,
    GLOSSARY_LOOKUP,
    PREPROCESS_TEXT,
    DETECT_SENTENCES,
    PROFILE_BASIC,
    PROFILE_FULL,
    TRANSLATE_TEXT,
    TRUSTED_SEARCH,
)


def parse_document_file(document_filename: str, shared_datadir) -> Document:
    # Load document from local file system
    path = Path(shared_datadir / document_filename)
    result: Document = Document.parse_file(path)

    return result


def test_analyze_build_configurations():

    cfg1 = AnalysisConfig(enable=["tok2vec"], disable=["senter"])
    cfg2 = AnalysisConfig(enable=["parser"], disable=["tagger"])

    assert (cfg1 + cfg1).enable == ["tok2vec"]
    assert (cfg1 + cfg1).disable == ["senter"]

    assert (cfg1 + cfg2).enable == ["tok2vec", "parser"]
    assert (cfg1 + cfg2).disable == ["senter", "tagger"]

    for lang in ["en", "de", "pt", "ru"]:
        assert PREPROCESS_TEXT[lang].enable == ["summed_preprocess_text"]

        # Detect sentences must contain "senter"
        assert "pysbd_sentencizer" in DETECT_SENTENCES[lang].enable
        # As the summary needs sentence detection, combining these two should result in the same enabled pipeline
        assert (DETECT_SENTENCES[lang] + CREATE_SUMMARY[lang]).enable == CREATE_SUMMARY[
            lang
        ].enable

        # Trusted search needs summarizer etc.
        assert set(
            [
                "pysbd_sentencizer",
                "summed_summarizer",
                "summed_trusted_search",
            ]
        ).issubset(TRUSTED_SEARCH[lang].enable)

        # Basic Profile: fast and cheap (no payd API calls) creation of summary
        assert not ["summed_gpt3_summarizer"] in PROFILE_BASIC[lang].enable


def test_analyze_simple_text_split_sentences(
    platform: SumMedPlatform, document_simple_file_en: Document
):

    document: Document = document_simple_file_en

    analyzer = Analyzer(platform)
    result: Document = analyzer.analyze(document, DETECT_SENTENCES)

    assert result.language == "en"
    assert result.source_file.filename == "simple_test_en.txt"
    assert result.source_file.content_type == "text/plain"

    # Test sentencizer result
    assert result.sentences is not None

    assert len(result.sentences) == 2
    assert result.sentences == ["This is just a very simple test for us.", "And the second sentence of this simple test."]
    assert result.sentences_lemma == ["simple test", "second sentence simple test"]


@pytest.mark.needs_internet
def test_analyze_different_languages_html_articles(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):
    extractor = Extractor(platform)
    analyzer = Analyzer(platform)

    # Load and analyze a german health article
    german_article = space.upload(
        "https://www.californiaprotons.com/de/breast-cancer/prevention-causes-risk-factors"
    )
    doc_de = analyzer.analyze(extractor.extract(german_article), CREATE_SUMMARY)

    assert doc_de.language == "de"
    assert doc_de.title.index("Verhindern Sie Brustkrebs") >= 0
    assert doc_de.summary

    # Load and analyze portugese health article
    portugese_article = space.upload(
        "https://www.californiaprotons.com/pt/breast-cancer/prevention-causes-risk-factors"
    )
    doc_pt = analyzer.analyze(extractor.extract(portugese_article), CREATE_SUMMARY)
    assert doc_pt.language == "pt"
    assert doc_pt.summary

    # Load and analyze russian health article
    russian_article = space.upload(
        "https://www.californiaprotons.com/ru/breast-cancer/prevention-causes-risk-factors"
    )

    # Unfortunatly, russian is not avialable for summaries
    # TODO need to do a translation first (or better russian model that supports noun_chunks (required by pytextrank)
    with pytest.raises(Exception):
        doc_pt = analyzer.analyze(extractor.extract(russian_article), CREATE_SUMMARY)
    # assert doc_pt.language == "ru"
    # assert doc_pt.summary


def test_analyze_different_languages_simple_sentence_splitting(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):

    analyzer = Analyzer(platform)

    doc_de: Document = parse_document_file("lang_de_01.json", shared_datadir)
    doc_pt: Document = parse_document_file("lang_pt_01.json", shared_datadir)
    doc_ru: Document = parse_document_file("lang_ru_01.json", shared_datadir)

    doc_de: Document = analyzer.analyze(doc_de, DETECT_SENTENCES)
    doc_pt: Document = analyzer.analyze(doc_pt, DETECT_SENTENCES)
    doc_ru: Document = analyzer.analyze(
        doc_ru, DETECT_SENTENCES
    )  # NotImplemented Error : noun_chunks

    assert doc_de.language == "de"
    assert doc_pt.language == "pt"
    assert doc_ru.language == "ru"  # NotImplemented Error : noun_chunks

    assert doc_de.metadata["pipeline_id"] == "de_core_news_sm"
    assert doc_de.sentences == ["Dies ist nur ein sehr einfacher Test für uns.", "Und der zweite Satz dieses einfachen Tests."]
    assert doc_de.sentences_lemma == ["einfach Test", "Satz einfach Test"]

    assert doc_pt.metadata["pipeline_id"] == "pt_core_news_sm"
    assert doc_pt.sentences == ["Este é apenas um teste muito simples para nós.", "E a segunda frase deste teste simples."]
    assert doc_pt.sentences_lemma == ["testar simples", "frase testar simples"]

    assert doc_ru.metadata["pipeline_id"] == "ru_core_news_sm"
    assert doc_ru.sentences == ["Это всего лишь очень простой тест для нас.", "И второе предложение этого простого теста."]
    assert doc_ru.sentences_lemma == ["лишь очень простой тест", "второй предложение простой тест"]


def test_analyze_html_page_sentenceing(
    platform: SumMedPlatform, document_sentencing_basic_test_en: Document
):

    document = document_sentencing_basic_test_en
    document = Analyzer(platform).analyze(document, PREPROCESS_TEXT)
    document = Analyzer(platform).analyze(document, DETECT_SENTENCES)

    assert document.language == "en"
    assert document.title == "Sentencing Basic Test - EN"
    assert document.author == "Zapp Brannigan"
    assert not document.summary

    # "at least more than 30 chars"   ==>   is_good == False :
    # assert "This is a simple HTML article." in document.sentences
    
    # "at least more than 5 words"   ==>   is_good == False :
    # assert "Sentences can span multiple lines." in document.sentences
    
    # "Needs to end with a dot"   ==>   is_good == False :
    # assert "Here's a list of things, let's see how this split: Point 1 Point 2" in document.sentences
    
    # This text was detected as three separate sentences :
    # assert (
    #     "We should be able to split sentences that contain: 1. multiple dots and interpunctation 2. lists and other things ... but still be just one sentence."
    #     in document.sentences
    # )


def test_analyze_summary(platform: SumMedPlatform, document_breast_cancer_en: Document):

    analyzer = Analyzer(platform)
    result: Document = analyzer.analyze(document_breast_cancer_en, CREATE_SUMMARY)

    assert result.summary
    assert len(result.summary) == 5  # The default
    logging.info("\n".join(result.summary))


def test_analyze_summary_from_file_url(
    platform: SumMedPlatform, space: ISpace, document_breast_cancer_en: Document
):

    # Analyze
    analyzer: Analyzer = Analyzer(platform)

    cfg: AnalysisConfig = CREATE_SUMMARY["en"].copy(deep=True)
    cfg.pipeline_config = {
        "summed_summarizer": {"num_sentences": 4, "preserve_order": True}
    }

    document = analyzer.analyze(document_breast_cancer_en, cfg)

    assert document.language == "en"

    assert len(document.summary) == 4

    assert document.sentences


def test_analyze_named_entities(
    platform: SumMedPlatform,
    document_breast_cancer_en: Document,
):

    document: Document = document_breast_cancer_en.copy(deep=True)

    document = Analyzer(platform).analyze(document, DETECT_ENTITIES)

    assert document.language == "en"
    assert document.entities
    assert not document.health_entities

    # Need a fresh copy, as the document is holding the state
    # document = document_breast_cancer_en.copy(deep=True)
    # document = Analyzer(platform).analyze(document, DETECT_HEALTH_ENTITIES)
    # assert document.health_entities
    # assert not document.entities


def test_analyze_named_entities_healthcare(
    platform: SumMedPlatform,
    document_breast_cancer_en: Document,
):

    document = document_breast_cancer_en

    document = Analyzer(platform).analyze(document, DETECT_HEALTH_ENTITIES)

    assert document.language == "en"
    assert document.health_entities


def test_analyze_gpt3_summary(
    platform: SumMedPlatform, document_breast_cancer_en: Document
):

    document = document_breast_cancer_en

    document = Analyzer(platform).analyze(document, CREATE_ABSTRACTIVE_SUMMARY)

    assert document.language == "en"
    assert document.abstractive_summary


def test_analyze_trusted_context_search(
    platform: SumMedPlatform, document_breast_cancer_en: Document
):
    document = document_breast_cancer_en

    document = Analyzer(platform).analyze(document, TRUSTED_SEARCH)

    assert document.language == "en"
    assert document.search_results


def test_analyze_trust_score(
    platform: SumMedPlatform, document_breast_cancer_en: Document
):
    document = document_breast_cancer_en

    document = Analyzer(platform).analyze(document, CALCULATE_TRUST_SCORE)

    assert document.language == "en"
    assert document.trust_score


def test_analyze_preprocess_text(
    platform: SumMedPlatform,
    document_breast_cancer_en: Document,
    document_news_article_cancer_en: Document,
):
    document = document_news_article_cancer_en

    text_raw = document.text
    document = Analyzer(platform).analyze(document, PREPROCESS_TEXT)
    assert document.text
    text_preprocessed = document.text

    # Preprocessing should be idempotent (e.g. multiple preprocess applications will not change the text)
    document = Analyzer(platform).analyze(document, PREPROCESS_TEXT["en"])
    text_preprocessed_2nd = document.text
    assert text_preprocessed == text_preprocessed_2nd

    # The raw text should be different from the preprocessed text
    assert text_raw != text_preprocessed


def test_analyze_translate_russian_and_back(
    platform: SumMedPlatform, document_simple_file_ru: Document
):
    document: Document = document_simple_file_ru
    analyzer: Analyzer = Analyzer(platform)

    assert document.language == None  # Language not yet detected
    assert document.original_language == None

    # Remember the orginal text
    original_text = document.text
    assert document.text == "Это всего лишь очень простой тест для нас. И второе предложение этого простого теста."

    # Translate to English
    document = analyzer.analyze(document, TRANSLATE_TEXT["en"])
    assert document.language == "en"
    assert document.metadata["translated_from"] == "ru"
    assert document.metadata["translated_to"] == ["en"]

    # Translate back to Russian
    document = analyzer.analyze(document, TRANSLATE_TEXT["ru"])
    assert document.language == "ru"
    assert document.original_language == "ru"
    assert document.metadata["translated_from"] == "ru"
    assert document.metadata["translated_to"] == ["en", "ru"]

    # Translate into the current language should not change anything
    document = analyzer.analyze(document, TRANSLATE_TEXT["ru"])
    assert document.language == "ru"
    assert document.original_language == "ru"
    assert document.metadata["translated_from"] == "ru"
    assert document.metadata["translated_to"] == ["en", "ru"]

    # Once again, this time portuguese
    document = analyzer.analyze(document, TRANSLATE_TEXT["pt"])
    assert document.language == "pt"
    assert document.original_language == "ru"
    assert document.metadata["translated_from"] == "ru"
    assert document.metadata["translated_to"] == ["en", "ru", "pt"]

    # Now back to russian
    document = analyzer.analyze(document, TRANSLATE_TEXT["ru"])
    assert document.language == "ru"
    assert document.original_language == "ru"
    assert document.metadata["translated_from"] == "ru"
    assert document.metadata["translated_to"] == ["en", "ru", "pt", "ru"]

    # I'd be surprised, but let's see how good the translators are...
    # assert document.text == original_text
    # Oo, this text is not so simple, so we need to check it manually :)


def test_analysis_portuguese_pdf_oncogenetica(
    platform: SumMedPlatform, document_pdf_portuguese_oncogenetica: Document
):
    document: Document = document_pdf_portuguese_oncogenetica
    analyzer: Analyzer = Analyzer(platform)

    assert document.language == "pt"  # Language detected on extraction
    assert document.original_language == None

    document = analyzer.analyze(document, PREPROCESS_TEXT)
    assert document.language == "pt"
    document = analyzer.analyze(document, DETECT_SENTENCES)
    document.text = " ".join(document.sentences)

    document = analyzer.analyze(document, TRANSLATE_TEXT["en"])
    assert document.language == "en"

    document = analyzer.analyze(document, CREATE_SUMMARY)
    document = analyzer.analyze(document, CREATE_ABSTRACTIVE_SUMMARY)
    document = analyzer.analyze(document, DETECT_ENTITIES)
    document = analyzer.analyze(document, DETECT_HEALTH_ENTITIES)
    document = analyzer.analyze(document, TRUSTED_SEARCH)
    document = analyzer.analyze(document, CALCULATE_TRUST_SCORE)

    assert document.language == "en"

    document_de = analyzer.analyze(document, TRANSLATE_TEXT["de"])
    document_ru = analyzer.analyze(document, TRANSLATE_TEXT["ru"])

    pass


def test_analysis_german_with_summaries_and_entities(
    platform: SumMedPlatform, document_news_article_cancer_de: Document
):
    document: Document = document_news_article_cancer_de
    analyzer: Analyzer = Analyzer(platform)

    assert document.language == None  # Language not yet detected
    assert document.original_language == None

    document = analyzer.analyze(document, PREPROCESS_TEXT)
    assert document.language == "de"

    # Translate to English, then analyze
    document = analyzer.analyze(document, TRANSLATE_TEXT["en"])
    assert document.language == "en"

    document = analyzer.analyze(document, PROFILE_FULL)
    assert document.original_language == "de"
    assert document.language == "en"
    assert document.sentences
    assert document.sentences_lemma
    assert document.summary
    assert document.abstractive_summary
    assert document.entities
    assert document.health_entities
    assert document.title
    # assert document.search_results
    
    # Try an alternative options for the abstract summary, since using the default options
    #   returns an empty response from gpt3.
    #
    ## CREATE_ABSTRACT_SUMMARY Test GPT-3 models, settings etc. settings
    # see: https://beta.openai.com/docs/engines/gpt-3
    # https://beta.openai.com/docs/api-reference/completions
    gpt3_conf = {
        "engine": "text-curie-001",
        "prompt_prefix": "Summarize and explain this medical text for a second-grade student :",
        "temperature": 0.3,
        "max_tokens": 300,
        "top_p": 0.9,
        "frequency_penalty": 1.5,  # -2.0 ... 2.0
        "presence_penalty": 1.5,  # -2.0 ... 2.0
    }

    document = analyzer.analyze(
        document,
        CREATE_ABSTRACTIVE_SUMMARY["en"] % {"summed_gpt3_summarizer": gpt3_conf},
    )
    assert document.abstractive_summary

    # Translate back to German
    document = analyzer.analyze(document, TRANSLATE_TEXT["de"])
    assert document.language == document.original_language == "de"
    assert document.metadata["translated_to"] == ["en", "de"]

    # Let's check if all these things are still there and have been translated into german
    det: Detector = Detector(platform)
    assert det.detect_language(" ".join(document.sentences)) == "de"
    assert det.detect_language(" ".join(document.summary)) == "de"
    assert det.detect_language(" ".join(document.abstractive_summary)) == "de"

    # TODO depending on content and length, these might be too short to reliably detect
    # assert det.detect_language(document.entities[0].text) == "de"
    # assert det.detect_language(document.title) == "de"

    assert det.detect_language(document.health_entities[0].text) == "de"
    # TODO this sometimes gives search results in different languages (depending on the search)
    # assert det.detect_language(document.search_results[0].snippet) == "de"
    # Names are not translated, only the snippets
    # assert det.detect_language(document.search_results[0].name) == "en"


def test_analyze_custom_component_configurations(
    platform: SumMedPlatform, document_news_article_cancer_en: Document
):
    document: Document = document_news_article_cancer_en
    analyzer: Analyzer = Analyzer(platform)

    ## CREATE_SUMMARY Test different length etc. settings
    document = analyzer.analyze(
        document, CREATE_SUMMARY["en"] % {"summed_summarizer": {"num_sentences": 3}}
    )
    assert len(document.summary) == 3

    document = analyzer.analyze(
        document,
        CREATE_SUMMARY["en"]
        % {"summed_summarizer": {"num_sentences": 7, "preserve_order": True}},
    )
    assert len(document.summary) == 7

    ## CREATE_ABSTRACT_SUMMARY Test GPT-3 models, settings etc. settings
    # see: https://beta.openai.com/docs/engines/gpt-3
    # https://beta.openai.com/docs/api-reference/completions

    gpt3_conf = {
        "engine": "text-curie-001",
        "prompt_prefix": "Summarize and explain this medical text for a second-grade student :",
        "temperature": 0.3,
        "max_tokens": 300,
        "top_p": 0.9,
        "frequency_penalty": 1.5,  # -2.0 ... 2.0
        "presence_penalty": 1.5,  # -2.0 ... 2.0
    }

    document = analyzer.analyze(
        document,
        CREATE_ABSTRACTIVE_SUMMARY["en"] % {"summed_gpt3_summarizer": gpt3_conf},
    )
    assert document.abstractive_summary


def test_analyze_english_pipeline_multiple_stages_enrichment(
    platform: SumMedPlatform,
    document_news_article_cancer_en: Document,
):
    document = document_news_article_cancer_en.copy(deep=True)
    assert not document.summary
    assert not document.language

    analyzer = Analyzer(platform)
    # Create the summary
    document = analyzer.analyze(document, CREATE_SUMMARY)
    assert document.language == "en"
    assert document.summary
    # assert document.model_id == "en_new"

    document = analyzer.analyze(document, DETECT_ENTITIES)
    assert document.entities

    document = analyzer.analyze(document, DETECT_HEALTH_ENTITIES)
    assert document.health_entities

    document = analyzer.analyze(document, CREATE_ABSTRACTIVE_SUMMARY)
    assert document.abstractive_summary

    document = analyzer.analyze(document, TRUSTED_SEARCH)
    assert document.search_results

    document = analyzer.analyze(document, CALCULATE_TRUST_SCORE)
    assert document.trust_score


def test_analyze_english_glossary_lookup(
    platform: SumMedPlatform,
    document_news_article_cancer_en: Document,
):
    analyzer = Analyzer(platform)

    document = document_news_article_cancer_en
    # Add new glossary
    assert not document.glossary
    document = analyzer.analyze(document, GLOSSARY_LOOKUP)
    assert document.glossary is not None  # ... but should be empty

    # Add a term to the glossary, but without explanation
    document.glossary["cancer"] = TermExplanation(term="cancer")
    assert document.glossary["cancer"] is not None
    assert not document.glossary["cancer"].explanation
    # Run the GLOSSARY LOOKUP, it will fill in the explanation for all missing terms
    document = analyzer.analyze(document, GLOSSARY_LOOKUP)
    assert document.glossary["cancer"].explanation

    # Make sure we have a source set
    assert document.glossary["cancer"].source

    # document = analyzer.analyze(
    #    document, PipelineFactory.CREATE_TRANSLATION({"to": "pt"})
    # )
    # assert document.language == "pt"
    # assert document.abstractive_summary


def test_analyze_abstractive_summary_for_url_article(
    platform: SumMedPlatform, space: ISpace
):
    extractor = Extractor(platform)
    analyzer = Analyzer(platform)

    url = "https://www.californiaprotons.com/breast-cancer/prevention-causes-risk-factors/"

    # Load it into our "space"
    source_file = space.upload(url)
    
    # and then extract it as a new document 
    document = extractor.extract(source_file)

    # Create a summary of the document
    # document = analyzer.analyze (document, CREATE_SUMMARY)

    # Create n "abstractive" (paraphrasing) summary of the document
    document = analyzer.analyze(document, CREATE_ABSTRACTIVE_SUMMARY)
    
    assert document.language == "en"
    assert document.abstractive_summary
