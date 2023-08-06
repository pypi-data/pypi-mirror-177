from summed.data import Document, FileInfo

from summed.extraction import IExtractorStrategy


class AudioTranscribeStrategy(IExtractorStrategy):
    def can_handle(self, source_file: FileInfo) -> bool:
        return (
            source_file.content_type and source_file.content_type[:5] == "audio"
        )  # e.g. audio/wav or audio/mp3

    def extract_from_bytes(self, data: bytes, document: Document) -> Document:
        return document
