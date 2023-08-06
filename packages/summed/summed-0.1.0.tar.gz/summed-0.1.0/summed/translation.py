import logging
import uuid

import requests
from langcodes import standardize_tag
from pydantic import BaseModel

from summed.summed_platform import SumMedPlatform
from summed.detector import Detector

class AzureTranslator(BaseModel):
    # See Azure Translator service docs:
    # https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?tabs=python

    platform: SumMedPlatform
    headers: str = None
    service_url: str = None

    def __init__(self, platform: SumMedPlatform, **kwargs):
        super().__init__(platform=platform, **kwargs)

        # Take variables from platform configuration
        subscription_key = self.platform.config.azure_translation_api_key
        endpoint = self.platform.config.azure_translation_api_endpoint
        location = self.platform.config.azure_translation_api_location

        # Prepare 'headers' for future calls
        self.headers = {
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Ocp-Apim-Subscription-Region": location,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }
        # Prepare 'service_url' for future calls
        self.service_url = endpoint + "/translate?api-version=3.0"
        pass

    def translate(self, text : str, target_language : str) -> str:
        """Translates a text string into the target language.
        If the target language is not valid, attemts to convert it to a valid value. If this is impossible, returns the original text.

        Args:
            text (_type_): Text to translate
            target_language (_type_): target language code, e.g. "de" or "ru"
                See https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/language-support

        Raises:
            e: Internet translation service is not available.

        Returns:
            str: The translated text
        """
        # Try to standardize target_language value
        try:
            target_language = standardize_tag(target_language)
        except ValueError:
            logging.error(f"{target_language} is not a supported language code")
            return text
        
        # Detect and standardize language of the text
        source_language = standardize_tag(Detector(self.platform).detect_language(text))
        
        # If the text does not need to be translated
        if source_language == target_language:
            return text

        # Create the full URL
        constructed_url = (
            self.service_url + "&from=" + source_language + "&to=" + target_language
        )
        # Create the body of the request with the text to be translated
        body = [{"text": text}]

        try:
            # Make the call using post
            translator_request = requests.post(
                constructed_url, headers=self.headers, json=body
            )
            # Retrieve the JSON response
            translator_response = translator_request.json()
            # Retrieve the translation
            translated_text = translator_response[0]["translations"][0]["text"]

            return translated_text
        except Exception as e:
            logging.error(f"Could not translate text: {e}. Internet translation service is not available.")
            raise e
