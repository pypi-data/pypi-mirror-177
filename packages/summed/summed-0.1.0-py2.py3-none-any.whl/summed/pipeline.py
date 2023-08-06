import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
from unittest.mock import DEFAULT
from langcodes import DEFAULT_LANGUAGE

from pydantic import BaseModel
from spacy.language import Language

from summed.data import Document
from summed.detector import Detector
from summed.summed_platform import IPlatform, SumMedPlatform

# -------------------------------------
# See: https://spacy.io/usage/processing-pipelines#example-stateful-components


class IPipelineFactory(ABC):
    @abstractmethod
    def select_pipeline_for_document(
        document: Document, config: Dict[str, Dict[str, str]] = {}
    ) -> Language:
        raise NotImplementedError()


class PipelineFactory(BaseModel, IPipelineFactory):
    """
    Selects the correct spaCy Language and pipeline for a language or document.
    The actual spaCy model is loaded and by the platform

    see:
    https://spacy.io/usage/processing-pipelines#plugins
    https://spacy.io/usage/processing-pipelines#custom-components-attributes

    https://spacy.io/usage/processing-pipelines#component-example3

    """

    model_by_language_code: Dict[str, str] = {
        "en": "en_core_sci_sm",  # "en_core_web_sm",
        "de": "de_core_news_sm",
        "pt": "pt_core_news_sm",
        "ru": "ru_core_news_sm",
        "xx": "xx_sent_ud_sm",
    }

    platform: SumMedPlatform = None

    def __init__(self, platform: IPlatform, **kwargs):
        super().__init__(platform=platform, **kwargs)
        self.platform = platform

    def get_default_pipeline_for_language(self, language: str) -> str:
        """
        Returnes the default pipeline package id for a language (used for a language if not explicity overridden by AnalysisConfig.pipline_package)
        TODO: make this configurable, discover available/installed packages etc.
        """
        return self.model_by_language_code.get(language, None)

    def select_pipeline_for_document(
        self, document: Document, config: Dict[str, Dict[str, str]] = {}
    ) -> Language:
        """Loads the internal spaCy Language model.


        Args:
            document (Document): our document. We'll decide which model to load/configure based on the document's language and potentially other hints in the document's metadata.

        Raises:
            ValueError: _description_

        Returns:
            Language: spaCy Language model, ready to use
        """
        try:
            # Take the language from the document. Try to detect if not set yet.
            language_code = (
                document.language
                or Detector(self.platform).detect_language(document.text)
                or None
            )

            model: Language = None
            # TODO document and test how we can override the automatic detection
            # pipeline_package = document.metadata.get("spacy_pipeline_package") or None
            # if not pipeline_package:

            pipeline_package = self.get_default_pipeline_for_language(language_code)

            if not pipeline_package:
                raise ValueError(
                    f"Can't find a matching pipeline package for language = '{language_code}'"
                )
            else:
                logging.info(f"Loading spaCy pipeline package '{pipeline_package}' ...")

            # This could take a few moments
            try:
                model = self.platform.configure_spacy_model(pipeline_package, config)
                if model is None:
                    raise ValueError(
                        f"Couldn't load spaCy model for pipeline package = '{pipeline_package}'"
                    )
                else:
                    logging.info(f"Loaded pipeline package '{pipeline_package}'")
            except Exception as e:
                raise Exception(
                    f"Error loading spaCy pipeline package '{pipeline_package}' : {e}"
                )

            assert model

            logging.info(
                f"Full pipeline of model '{pipeline_package}' : {model.pipe_names}"
            )

            return model

        except Exception as e:
            logging.warning(f"Error while loading language model: {e}")
            raise ValueError(e)
