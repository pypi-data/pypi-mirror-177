import logging
import re


from summed.data import Document, FileInfo
from summed.extraction import IExtractorStrategy
from summed.extraction.form_recognizer import FormRecognizerStrategy


class ImageOcrStrategy(IExtractorStrategy):
    def can_handle(self, source_file: FileInfo) -> bool:
        # accept image files up to 10MB
        return (
            re.match("image/", source_file.content_type)
            and source_file.size > 0
            and source_file.size <= 1024 * 1024 * 10
        )

    def extract_from_bytes(self, data: bytes, document: Document) -> Document:
        logging.info("Extracting text from image")
        if self.platform.has_form_recognizer:
            logging.info("Using Azure Form Recognizer for image OCR")
            return FormRecognizerStrategy(self.platform).extract_from_bytes(
                data, document
            )
        else:
            logging.error(f"ImageOcr not implemented if Form recognizer is unavailable")

        return document
