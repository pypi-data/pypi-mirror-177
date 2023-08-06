import logging
import re


from summed.data import Document, FileInfo
from summed.extraction import IExtractorStrategy
from summed.extraction.form_recognizer import FormRecognizerStrategy


class DocxStrategy(IExtractorStrategy):
    def can_handle(self, source_file: FileInfo) -> bool:
        # accept image files up to 10MB
        return (
            re.match(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                source_file.content_type,
            )
            and source_file.size > 0
            and source_file.size <= 1024 * 1024 * 10
        )

    def extract_from_bytes(self, data: bytes, document: Document) -> Document:
        logging.info("Extracting text from word document (docx format)")
        if self.platform.has_form_recognizer:
            logging.info("Using Azure Form Recognizer for extraction")
            return FormRecognizerStrategy(self.platform).extract_from_bytes(
                data, document
            )
        else:
            logging.error(
                f"Word/docx extraction not implemented if Form recognizer is unavailable"
            )

        return document
