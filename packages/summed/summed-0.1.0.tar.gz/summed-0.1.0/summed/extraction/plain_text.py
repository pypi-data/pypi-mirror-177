import re


from summed.data import Document, FileInfo
from summed.summed_platform import SumMedPlatform
from summed.utils import collapse_whitespace

from summed.extraction import ExtractorPluginSpec, IExtractorStrategy


# @ExtractorPluginSpec.summed_extractor_factory
# def text_extractor_factory(platform: SumMedPlatform, **kwargs) -> IExtractorStrategy:
#     logging.info(f"Creating Plain Text extractor")
#     return PlainTextStrategy(platform, **kwargs)


class PlainTextStrategy(IExtractorStrategy):
    def can_handle(self, source_file: FileInfo) -> bool:
        return re.match("text/plain", source_file.content_type)

    def extract_from_bytes(self, data: bytes, document: Document) -> Document:

        document.text = collapse_whitespace(
            data.decode("utf-8")
        )  # TODO: handle different encodings
        document.title = document.source_file.filename or document.text.split("\n")[0]

        return document
