import collections
import logging
import re
from abc import ABC, abstractmethod
from asyncio.log import logger
from cgitb import enable
from platform import platform
from typing import Dict, List, Union

import pytextrank

import spacy
from pydantic import BaseModel
from spacy.language import Language
from spacy.tokens.doc import Doc

from summed.data import AnalysisConfig, Document, FileInfo, NamedEntity
from summed.detector import Detector
from summed.pipeline import PipelineFactory
from summed.summed_platform import IPlatform, SumMedPlatform


class IAnalyzer(ABC):
    @abstractmethod
    def __init__(self, platform: IPlatform, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def analyze(
        self, document: Document, config: AnalysisConfig, overwriteExisting=False
    ) -> Document:
        raise NotImplementedError()


class Analyzer(BaseModel, IAnalyzer):
    """Analyzer is the key component of the analysis process. It is responsible for "enriching" the document, based on some analysis configuration.
    The Analysis configuration is a set of parameters that define the parts of the spaCy pipeline to run, depending on configuration and document properties, especially the language.

    """

    platform: SumMedPlatform = None

    def __init__(self, platform: IPlatform, **kwargs):
        super().__init__(platform=platform, **kwargs)
        self.platform = platform

    def preprocess_text(self, document: Document) -> Document:
        """Preprocess document text before further analysis.
        This is defensive, but potentially destructive to the original text.
        e.g. to filter out extraction errors and artifacts, unprocessable characters,

        Args:
            document (str): original document containing the original text

        Returns:
            str: pre-processed version of document.text, hopefully better suited for further analysis
        """

        # Collapse whitespace
        preprocessed = document.text.replace("\r", " ")
        preprocessed = document.text.replace("\n", " ")
        preprocessed = document.text.replace("\t", " ")
        preprocessed = re.sub(r"\s+", " ", preprocessed)

        # Numbered lists 1. 2. ... => (1) (2)
        preprocessed = re.sub(r"\s(\d)\. ", " (\\1) ", preprocessed)

        document.text = preprocessed.strip()

        return document

    def extract_entities(self, spacy_doc: Doc) -> List[NamedEntity]:

        # from spacy.pipeline.ner import DEFAULT_NER_MODEL

        # see https://spacy.io/api/entityrecognizer

        # config = {
        #     "moves": None,
        #     "update_with_oracle_cut_size": 100,
        #     "model": DEFAULT_NER_MODEL,
        #     "incorrect_spans_key": "incorrect_spans",
        # }
        # nlp.add_pipe("ner", config=config)
        entities = []
        for ent in spacy_doc.ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
            entities.append((ent.text, ent.label_))

        result = collections.Counter(entities)

        # Return the entities, orded from most frequent to least frequent
        return sorted(
            [
                NamedEntity(text=ent[0], label=ent[1], count=count)
                for ent, count in result.items()
            ],
            key=lambda ne: ne.count,
            reverse=True,
        )

    def analyze(
        self,
        input_document: Document,
        analysis_config: Union[AnalysisConfig, Dict[str, AnalysisConfig]],
        pipeline_config: Dict[str, Dict[str, str]] = {},
        force_overwrite=False,
    ) -> Document:
        """Analyze the given document.

        Args:
            document (Document): the document to analyze. This can be iterativly applied.

        Returns:
            Document: Document with additional analysis results.
        """

        # If necessary, detect the language here

        document = input_document.copy(deep=True)
        try:

            document.language = document.language or Detector(
                self.platform
            ).detect_language(document.text)
        except Exception as e:
            logging.warning(
                f"Can't detect language - document.text too short ? : {document.text}"
            )

        # For convenience, take the AnalysisConfig out of a language-specific dict ("en" -> AnalysisConfig(...))
        if isinstance(analysis_config, dict):
            config = analysis_config.get(document.language)
        else:
            config = analysis_config
        if not config:
            raise ValueError(
                f"No analysis config available for language {document.language}"
            )

        try:
            # Load the spaCy NLP "Language" . Must match the document/text language
            # The factory is responsible for selecting and loading the correct language model via the platform.
            nlp = PipelineFactory(self.platform).select_pipeline_for_document(
                document, config=pipeline_config
            )

            # Add pipeline metadata to document. TODO maybe make this append-only
            document.metadata["pipeline_id"] = f"{nlp.meta['lang']}_{nlp.meta['name']}"
            document.metadata["pipeline_names"] = f"{nlp.pipe_names}"
            document.metadata["pipeline_config"] = f"{config.pipeline_config}"

        except Exception as e:
            logging.error(
                f"Failed to load selected spaCy pipeline for language '{document.language}': {e}"
            )
            return document

        # We really should have a spaCy pipeline at  this point
        assert nlp is not None

        # Step 1. preprocess text
        # TODO this should go into a spearate Language component that modifies the document.text
        # We replace the "original", so from here on, document.text may differ from what was originally extracted
        # Only preprocess text if metadata[text_preprocessed] is not True
        # if not document.metadata.get("text_preprocessed") or force_overwrite:
        #     logging.info(f"Preprocessing document text (once, unless forced)...")
        #     document = self.preprocess_text(document)
        #     document.metadata["text_preprocessed"] = True

        #
        # Step 2. create NLP parsing instance
        #
        # invert: from enabled pipes
        disable = [x for x in nlp.pipe_names if x not in config.enable] + config.disable
        logging.info(
            f"Running spaCy pipeline, with only these components: {[c for c in nlp.pipe_names if c not in disable]}..."
        )
        spacy_doc = nlp(
            document.text, disable=disable, component_cfg=config.pipeline_config
        )

        # if not Doc.has_extension("summed_platform"):
        #     Doc.set_extension("summed_platform", default=None, force=True)
        # if not Doc.has_extension("summed_current_document"):
        #     Doc.set_extension("summed_current_document", default=None, force=True)

        # spacy_doc._.summed_platform = self.platform
        # spacy_doc._.summed_current_document = document

        # Step 3. detect sentences
        # TODO: Here we can do advanced filtering to remove 'wrong' sentences, e.g.:
        # - remove sentences that are too short
        # - remove incomplete senteces (use POS), e.g. sentences without a

        ## TODO move this elsewhere - filter sentences and create lemmatized sentences
        if spacy_doc.sents:
            try:
                # extract splitted sentences
                document.sentences = [str(sent) for sent in spacy_doc.sents]
                #  lemmatization of sentences
                document.sentences_lemma = []
                good_sentences = []
                for sent in spacy_doc.sents:
                    token = spacy_doc[sent.start : sent.end]

                    # TODO this could be more sophisticated, e.g. use POS to make sufre we have "good" sentences
                    is_good = (
                        str(token)[-1:] == "."  # Needs to end with a dot  - but is it really reasonable?!
                        and len(str(token)) < 200  # max 200 chars
                        and len(str(token)) > 30  # at least more than 30 chars
                        and len(str(token).split()) > 5  # at least more than 5 words
                    )

                    if is_good:
                        good_sentences.append(str(token))
                        lemmatized_sentence = " ".join(
                            [t.lemma_ for t in token if not (t.is_stop or t.is_punct)]
                        ).strip()
                        document.sentences_lemma.append(lemmatized_sentence)

                # keep only good sentences
                document.sentences = good_sentences

            except Exception as e:
                logging.warning(f"Could not detect sentences, skipping: {e}")

        #  NER of text
        # TODO maybe put into a separate component?
        if spacy_doc.ents:
            document.entities = self.extract_entities(spacy_doc)

        # Step 6: Collects data from enabled spacy extensions into the Document

        # Go over all enabled pipeline components, and call their component function - IN ORDER.
        #
        #  TODO: Note that the enable=[...] order might not necessarly be the order of the component in nlp.pipe_names ! See platform.load_spacy_model(...)
        #
        # Each component function needs to be registered as a document customer attribute (doc._.my_extension)
        #
        # Will take 3 parameter:
        #   - platform: the platform instance, to access config and API clients
        #   - doc: the document to analyze (spacy.language.Doc). The piple has alredy so all enabled spacy pipes have executed.
        #          This is a second pass only over the extensions, so modifying this here is probably not very useful.
        #   - document: Our document. The component function will do whatever it has to do, and then update the document fields IN PLACE
        #
        try:
            for component in config.enable:
                # If there's an extension attribute with the same name as the component, get it

                if Doc.has_extension(component):
                    logging.info(f"Applying changes to document from '{component}' ...")
                    d = spacy_doc._.get(component)
                    component_result = (
                        d(self.platform, spacy_doc, document) if callable(d) else d
                    )
        except Exception as e:
            logging.error(f"Exception executing summed component '{component}': {e}")

        return document
