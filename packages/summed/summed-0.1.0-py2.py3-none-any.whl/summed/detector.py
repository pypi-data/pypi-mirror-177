import logging
import mimetypes
import os
from tkinter import N

from langdetect import DetectorFactory as _dt
from langdetect import detect_langs
from langcodes import standardize_tag
from pydantic import BaseModel

# deterministic results for langdetect
_dt.seed = 0


from charset_normalizer import detect as detect_encoding

from summed.summed_platform import SumMedPlatform


class Detector(BaseModel):
    """Helper class with methods for detecting things like language, encoding, content type etc. of files, urls or binary data"""

    platform: SumMedPlatform

    def __init__(self, platform: SumMedPlatform, **kwargs):
        super().__init__(platform=platform, **kwargs)

    def detect_language(self, text: str, default_language: str = 'en') -> str:
        """This is used for detecting language of the text, e.g. 'en' or other
        Uses https://pypi.org/project/langdetect/
        Args:
            text (str): The text to detect language of
            default_language (str, optional):  If detection/guessing fails or default_language is in multiple
                result of detecting, return this as defaul. Defaults to 'en'.
        Returns:
            str: The detected language

        """
       # Check the default language if it has been replaced by a valid language
        try:
            default_language = standardize_tag(default_language)
        except ValueError:
            logging.warning(f"{default_language} is not a supported language code. Chengeing to 'en'")
            default_language = 'en'

        try:
            langs = detect_langs(text)
            # do just for short texts, otherwise dafault_language option is not used
            if (len(langs) > 1) and (len(text) < 20):
                return default_language
            return langs[0].lang
        except Exception as e:
            logging.warning(f"Could not detect language of '{text}', defaulting to '{default_language}'")
            return default_language

    def detect_encoding(self, data: bytes) -> str:
        """This is used for detecting encoding of the binary data, e.g. UTF-8 or other
        Uses https://charset-normalizer.readthedocs.io/en/latest/

        Args:
            data (bytes): The bytes to check
        Returns:
            str: The detected encoding

        """
        result = detect_encoding(data)
        if not result:
            logging.warning(
                f"Could not detect encoding of the data, defaulting to 'utf-8'. Good luck!"
            )
        return result["encoding"] or "utf-8"

    def detect_content_type(
        self, source: str, default_content_type: str = "application/octet-stream"
    ) -> str:
        """
        Detects the content type (mime type) of e.g. a file, url etc.
        The content type is "guessed", e.g. by file extensions or content inspection of the data (if possible)

        Args:
            source (str): _description_
            default_content_type (str, optional):  If detection/guessing fails, return this as defaul. Defaults to "application/octet-stream".

        Returns:
            str: _description_
        """

        s = source.split("#")[0].split("?")[0].rstrip("/")
        basename = os.path.basename(s)
        guessed_content_type = mimetypes.guess_type(basename)[0]
        if guessed_content_type is None:
            # TODO - use a more reliable way to detect content type
            logging.warning(
                f"Could not guess content type for {s}, using {default_content_type}"
            )

        return guessed_content_type or default_content_type
