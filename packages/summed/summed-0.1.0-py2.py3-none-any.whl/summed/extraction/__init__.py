from abc import ABC, abstractmethod
import logging
import sys
from typing import Optional

from pydantic import BaseModel

from summed.summed_platform import SumMedPlatform
from summed.data import FileInfo, Document

import pluggy


class IExtractorStrategy(BaseModel, ABC):
    """
    Extractor strategies are responsible for extracting text and metadata from a file in a Space.
    They are used by the extractor to determine which strategy to use for a given file.
    Each strategy must indicate if it can handle the file, usually based on the file's content_type (e.g. text/html or application/pdf).
    In case multiple strategies can handle the file, the extractor may decide to use the first strategy that can handle the file.

    """

    # Extractor strategies may  not require a platform object.
    platform: Optional[SumMedPlatform] = None

    def __init__(self, platform: SumMedPlatform, **kwargs):
        super().__init__(platform=platform, **kwargs)
        self.platform = platform

    @abstractmethod
    def can_handle(self, source_file: FileInfo) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def extract_from_bytes(self, data: bytes, document: Document) -> Document:
        """Extracts (raw) text and metadata from a file in a space.
        Args:
            data (bytes): raw data of the file
            document (Document): Summed document, with text and metadata extracted from the file. Modified in-place

        Returns:
            Document: Alos returned, the document.
        """
        raise NotImplementedError()


# Specify and load all plugins
summed_extractor_hookspec = pluggy.HookspecMarker("summed_extractor_plugins")
summed_extractor = pluggy.HookimplMarker("summed_extractor_plugins")


class ExtractorPluginSpec:
    @summed_extractor_hookspec
    def summed_extractor_factory(
        self, platform: SumMedPlatform, **kwargs
    ) -> IExtractorStrategy:
        """
        Return an extractor strategy for the given platform.
        """
        pass


# extractor_plugins = pluggy.PluginManager("summed_extractor_plugins")
# extractor_plugins.add_hookspecs(ExtractorPluginSpec)

# extractor_plugins.register(sys.modules[__name__])


# extractors = extractor_plugins.list_name_plugin()  # hook.summed_extractor_factory()


from .audio_transcribe import (
    AudioTranscribeStrategy as audio_transcribe_strategy,
)
from .html_extract import HTMLStrategy as html_strategy
from .image_ocr import ImageOcrStrategy as image_ocr_strategy
from .form_recognizer import FormRecognizerStrategy as form_recognizer_strategy
from .plain_text import PlainTextStrategy as plain_text_strategy
from .docx_extract import DocxStrategy as docx_strategy
