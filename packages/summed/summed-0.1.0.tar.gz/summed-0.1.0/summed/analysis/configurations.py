from typing import Dict, List, Optional


from summed.data import AnalysisConfig


class EN(AnalysisConfig):
    pipeline_package: str = "en_core_sci_sm"
    enable: Optional[List[str]] = [
        "tok2vec",
        "tagger",
        "parser",
        "attribute_ruler",
        "lemmatizer",
        "pysbd_sentencizer",
    ]


class DE(AnalysisConfig):
    pipeline_package: str = "de_core_news_sm"
    enable: Optional[List[str]] = [
        "tok2vec",
        "tagger",
        "morphologizer",
        "parser",
        "senter",
        "attribute_ruler",
        "lemmatizer",
    ]


class PT(AnalysisConfig):
    pipeline_package: str = "pt_core_news_sm"
    enable: Optional[List[str]] = [
        "tok2vec",
        "morphologizer",
        "parser",
        "pysbd_sentencizer",
        "attribute_ruler",
        "lemmatizer",
    ]


class RU(AnalysisConfig):
    pipeline_package: str = "ru_core_news_sm"
    enable: Optional[List[str]] = [
        "tok2vec",
        "morphologizer",
        "parser",
        "senter",
        "attribute_ruler",
        "lemmatizer",
    ]


class XX(AnalysisConfig):
    pipeline_package: str = "xx_sent_ud_sm"
    enable: Optional[List[str]] = ["senter"]


# No NLP pipes enabled, just preprocess the text
PREPROCESS_TEXT = {
    "en": EN(enable=["summed_preprocess_text"]),
    "de": DE(enable=["summed_preprocess_text"]),
    "pt": PT(enable=["summed_preprocess_text"]),
    "ru": RU(enable=["summed_preprocess_text"]),
    "xx": XX(enable=[]),
}


DETECT_SENTENCES = {
    "en": EN() + AnalysisConfig(enable=["pysbd_sentencizer"]),
    "de": DE() + AnalysisConfig(enable=["pysbd_sentencizer"]),
    "pt": PT() + AnalysisConfig(enable=["pysbd_sentencizer"]),
    "ru": RU() + AnalysisConfig(enable=["pysbd_sentencizer"]),
    "xx": XX() + AnalysisConfig(enable=["pysbd_sentencizer"]),
}

CREATE_SUMMARY: Dict[str, AnalysisConfig] = {
    "en": DETECT_SENTENCES["en"]
    + AnalysisConfig(enable=["biasedtextrank", "summed_summarizer"]),
    "de": DETECT_SENTENCES["de"]
    + AnalysisConfig(enable=["biasedtextrank", "summed_summarizer"]),
    "pt": DETECT_SENTENCES["pt"]
    + AnalysisConfig(enable=["biasedtextrank", "summed_summarizer"]),
    "ru": DETECT_SENTENCES["ru"]
    + AnalysisConfig(enable=["biasedtextrank", "summed_summarizer"]),
}

CREATE_ABSTRACTIVE_SUMMARY = {
    "en": EN(enable=["summed_gpt3_summarizer"]),
    "de": DE(enable=["summed_gpt3_summarizer"]),
    "pt": PT(enable=["summed_gpt3_summarizer"]),
    "ru": RU(enable=["summed_gpt3_summarizer"]),
}

# Trusted search depends on the availability of the summary
TRUSTED_SEARCH = {
    "en": CREATE_SUMMARY["en"] + AnalysisConfig(enable=["summed_trusted_search"]),
    "de": CREATE_SUMMARY["de"] + AnalysisConfig(enable=["summed_trusted_search"]),
    "pt": CREATE_SUMMARY["pt"] + AnalysisConfig(enable=["summed_trusted_search"]),
    "ru": CREATE_SUMMARY["ru"] + AnalysisConfig(enable=["summed_trusted_search"]),
}

DETECT_ENTITIES = {
    "en": EN() + AnalysisConfig(enable=["ner"]),
    "de": DE() + AnalysisConfig(enable=["ner"]),
    "pt": PT() + AnalysisConfig(enable=["ner"]),
    "ru": RU() + AnalysisConfig(enable=["ner"]),
}


# Health entities only support english text, so we need to add a translator pipe for other languages
DETECT_HEALTH_ENTITIES = {
    "en": AnalysisConfig(enable=["summed_health_entities"]),
    "de": AnalysisConfig(enable=["summed_translation", "summed_health_entities"]),
    "pt": AnalysisConfig(enable=["summed_translation", "summed_health_entities"]),
    "ru": AnalysisConfig(enable=["summed_translation", "summed_health_entities"]),
}


GLOSSARY_LOOKUP = {
    "en": AnalysisConfig(enable=["summed_glossary_lookup"]),
    "de": AnalysisConfig(enable=["summed_translation", "summed_glossary_lookup"]),
    "pt": AnalysisConfig(enable=["summed_translation", "summed_glossary_lookup"]),
    "ru": AnalysisConfig(enable=["summed_translation", "summed_glossary_lookup"]),
}


###
# Translate the document into one of our supported languages.
# Will modify the document.text in place.
###
TRANSLATE_TEXT = {
    "en": AnalysisConfig(
        enable=["summed_translation"],
        pipeline_config={"summed_translation": {"target_lang": "en"}},
    ),
    "de": AnalysisConfig(
        enable=["summed_translation"],
        pipeline_config={"summed_translation": {"target_lang": "de"}},
    ),
    "pt": AnalysisConfig(
        enable=["summed_translation"],
        pipeline_config={"summed_translation": {"target_lang": "pt"}},
    ),
    "ru": AnalysisConfig(
        enable=["summed_translation"],
        pipeline_config={"summed_translation": {"target_lang": "ru"}},
    ),
}


CALCULATE_TRUST_SCORE = {
    "en": AnalysisConfig(enable=["summed_trust_score"]),
    "de": AnalysisConfig(enable=["summed_trust_score"]),
    "pt": AnalysisConfig(enable=["summed_trust_score"]),
    "ru": AnalysisConfig(enable=["summed_trust_score"]),
}


PROFILE_BASIC = {
    "en": PREPROCESS_TEXT["en"] + DETECT_SENTENCES["en"] + CREATE_SUMMARY["en"],
    "de": PREPROCESS_TEXT["de"] + DETECT_SENTENCES["de"] + CREATE_SUMMARY["de"],
    "pt": PREPROCESS_TEXT["pt"] + DETECT_SENTENCES["pt"] + CREATE_SUMMARY["pt"],
    "ru": PREPROCESS_TEXT["ru"] + DETECT_SENTENCES["ru"] + CREATE_SUMMARY["ru"],
}


PROFILE_FULL = {
    "en": PROFILE_BASIC["en"]
    + CREATE_ABSTRACTIVE_SUMMARY["en"]
    + DETECT_ENTITIES["en"]
    + DETECT_HEALTH_ENTITIES["en"]
    + TRUSTED_SEARCH["en"]
    + CALCULATE_TRUST_SCORE["en"]
    + GLOSSARY_LOOKUP["en"],
    "de": PROFILE_BASIC["de"]
    + CREATE_ABSTRACTIVE_SUMMARY["de"]
    + DETECT_ENTITIES["de"]
    + DETECT_HEALTH_ENTITIES["de"]
    + TRUSTED_SEARCH["de"]
    + CALCULATE_TRUST_SCORE["de"]
    + GLOSSARY_LOOKUP["de"],
    "pt": PROFILE_BASIC["pt"]
    + CREATE_ABSTRACTIVE_SUMMARY["pt"]
    + DETECT_ENTITIES["pt"]
    + DETECT_HEALTH_ENTITIES["pt"]
    + TRUSTED_SEARCH["pt"]
    + CALCULATE_TRUST_SCORE["pt"]
    + GLOSSARY_LOOKUP["pt"],
    "ru": PROFILE_BASIC["ru"]
    + CREATE_ABSTRACTIVE_SUMMARY["ru"]
    + DETECT_ENTITIES["ru"]
    + DETECT_HEALTH_ENTITIES["ru"]
    + TRUSTED_SEARCH["ru"]
    + CALCULATE_TRUST_SCORE["ru"]
    + GLOSSARY_LOOKUP["ru"],
}
