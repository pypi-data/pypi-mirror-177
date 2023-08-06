from abc import ABC, abstractmethod
import logging
from pydoc import TextDoc
import re
from typing import Dict, List

from pydantic import BaseModel
from summed import extraction
from summed.data import DocumentSource, FileInfo, Document

# from summed.detector import Detector


# TODO Discover all strategies dynamically
from summed.extraction import IExtractorStrategy

from summed.extraction import (
    plain_text,
    html_strategy,
    audio_transcribe_strategy,
    image_ocr_strategy,
    form_recognizer_strategy,
    docx_strategy,
)

from summed.summed_platform import IPlatform, SumMedPlatform
from summed.space import ISpace, Space

from bs4 import BeautifulSoup
from boilerpy3 import extractors
from boilerpy3.document import TextDocument


from summed.utils import collapse_whitespace


# can be used in lambda expression
def raise_error(ex):
    raise ex


class IExtractor(ABC):
    """
    Extractors are the first step in our analysis pipeline. It takes a FileInfo object (blob stored in a space) and created a Document object.
    They are responsible for extracting the text and metadata from the file.
    This usually involves detection of the file content_type, as extraction strategies are handled differently for different content types.

    """

    @abstractmethod
    def extract(self, source_file: FileInfo) -> Document:
        """Extracts (raw) text and metadata from a file in a space.
        Args:
            source_file (FileInfo): source file in a space

        Returns:
            Document: SumMed document, with text and metadata extracted from the file
        """

        raise NotImplementedError()

    @abstractmethod
    def can_handle(self, source_file: FileInfo) -> bool:
        raise NotImplementedError()


class Extractor(BaseModel, IExtractor):
    """
    Extractors are the first step in our analysis pipeline. It takes a FileInfo object (blob stored in a space) and creates a Document object.
    They are responsible for extracting the text and metadata from the file.
    This usually involves detection of the file content_type, as extraction strategies are handled differently for different content types.

    TODO: In the future, there might be extension points here for custom content types, known-document preferences, policies (quick, cheapest), etc.
    """

    strategy_list: List[IExtractorStrategy] = None
    platform: SumMedPlatform = None

    def __init__(self, platform: SumMedPlatform, **kwargs):
        """
        Creates a new extractor, to extract text and metadata from files in a space.


        Args:
            platform (SumMedPlatform): The summed platform to use, with access to configuration and shared resources
        """
        super().__init__(platform=platform, **kwargs)

        self.platform = platform

        # TODO make this configurable / extenable
        self.strategy_list: self.strategy_list or List[IExtractorStrategy] = [
            extraction.plain_text_strategy(self.platform),
            extraction.html_strategy(self.platform),
            extraction.form_recognizer_strategy(self.platform),
            extraction.image_ocr_strategy(self.platform),
            extraction.docx_strategy(self.platform),
            extraction.audio_transcribe_strategy(self.platform),
        ]

    def can_handle(self, source_file: FileInfo) -> bool:
        return self._determine_extraction_strategy(source_file) is not None

    def _determine_extraction_strategy(
        self, source_file: FileInfo
    ) -> IExtractorStrategy:
        """
        Determine the extraction strategy to use for a given file.

        """
        # TODO for now, we just take take the first strategy that can handle the file
        for strategy in self.strategy_list:
            if strategy.can_handle(source_file):
                logging.info(
                    f"Selected extraction strategy: {strategy.__class__.__name__} "
                )
                return strategy

        return None

    def extract(self, source_file: FileInfo) -> Document:
        """
        Extracts text and metadata from a file, and returns a Document for further analysis.
        Will ALWAYS overwrite document.text field

        Args:
            source_file (FileInfo): FileInfo object identifying the source file from a Space

        Returns:
            Document: the extracted document
        """

        # Inititalize new document with the reference to the source_file from our space
        document = Document(source_file=source_file)

        # Determine the extraction strategy to use
        extractor_strategy: IExtractorStrategy = self._determine_extraction_strategy(
            source_file
        )

        if not extractor_strategy:
            raise_error(
                Exception(
                    f"No extraction strategy for '{source_file.content_type}' found: {source_file}"
                )
            )

        # Call the handler strategy
        try:
            # Load file content as bytes
            # FIXME:how do we select the right space here ? get from platform?
            data = Space(self.platform).download(source_file)
            # Call the strategy handler for the content type
            document = extractor_strategy.extract_from_bytes(data, document)
            # we may detect the language of the document there...
            # document.language = Detector(self.platform).detect_language(document.text)

        except Exception as ex:
            logging.error(f"Could not extract from '{source_file.filename}': {ex} ")

        # Normalize to empty string
        if not document.text:
            document.text = ""

        return document
