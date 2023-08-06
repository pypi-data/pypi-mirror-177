# import importlib
import importlib
import logging

from abc import ABC, abstractmethod
from datetime import datetime

from importlib.metadata import version
from typing import Dict, List, Optional, Union

import spacy
import requests


from pydantic import BaseModel, validator


# A bit confusion with client libs bing vs cognitive services
# See: https://docs.microsoft.com/en-us/bing/search-apis/bing-custom-search/quickstarts/sdk/custom-search-client-library-python
# https://github.com/Azure-Samples/cognitive-services-python-sdk-samples

from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.textanalytics import TextAnalyticsClient

from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    __version__,
)

from summed.data import PlatformConfig
from summed.utils import import_module_by_name


#
# Platform is a central object to all the other parts of the system.
# The idea is that it holds all the shared configuration and models for the different parts of (blob service, external API clients, spaCy Language models etc...), and can be reused by
# multiple calls to extractors, analyzer etc.
#
#
class IPlatform(ABC):

    pass


class SumMedPlatform(BaseModel, IPlatform):
    """
    SumMed Platform , used to access global platform state like credentials, extensions.
    """

    config: PlatformConfig = None

    # Internal fields for shared objects that we hold
    _azure_blob_service_client: BlobServiceClient = None
    _azure_form_recognizer_client: FormRecognizerClient = None
    _azure_text_analytics_client: TextAnalyticsClient = None
    _bing_custom_search_client: requests.Session = None
    # This is just a REST client sessions (for now)
    _dictionary_client: requests.Session = None

    # Register the spaCy language models. We hold one per language, Analyis is then execution (sub) pipelines with config, depending on task
    # Don't do spacy.load(...) more than once
    _spacy_models: Dict[str, spacy.Language] = {}

    @property
    def has_openai_gpt3(self) -> bool:
        return self.config.openai_api_key is not None

    @property
    def has_cognitive_services(self) -> bool:
        return self.config.azure_cognitive_services_api_key is not None

    @property
    def has_form_recognizer(self) -> bool:
        return self.config.azure_form_recognizer_api_key is not None

    @property
    def has_translator(self) -> bool:
        return self.config.azure_cognitive_services_api_key is not None

    @property
    def has_trusted_search(self) -> bool:
        return self.config.bing_custom_search_api_key is not None

    @property
    def has_text_analytics_for_health(self) -> bool:
        return self.config.azure_cognitive_services_api_key is not None

    @property
    def has_dictionary(self) -> bool:
        return self.config.mw_medical_dictionary_api_key is not None

    @property
    def has_immersive_reader(self) -> bool:
        return self.config.azure_immersive_reader_tenant_id is not None

    def get_azure_blob_service_client(self) -> BlobServiceClient:
        if self._azure_blob_service_client is None:
            try:
                logging.info("Creating Azure blob service client")

                self._azure_blob_service_client = (
                    BlobServiceClient.from_connection_string(
                        conn_str=self.config.azure_storage_connection_string
                    ).get_container_client(self.config.azure_storage_container)
                )

            except Exception as e:
                logging.error(f"Can't create Azure blob service client: {e}")
                self._azure_blob_service_client = None

        return self._azure_blob_service_client

    def get_azure_form_recognizer_client(self) -> FormRecognizerClient:
        if self._azure_form_recognizer_client is None:
            try:
                logging.info("Creating Azure form recognizer client")

                self._azure_form_recognizer_client = FormRecognizerClient(
                    endpoint=self.config.azure_form_recognizer_api_endpoint,
                    credential=AzureKeyCredential(
                        self.config.azure_form_recognizer_api_key
                    ),
                )

            except Exception as e:
                logging.error(f"Can't create Azure form recognizer client: {e}")
                self._azure_form_recognizer_client = None

        return self._azure_form_recognizer_client

    def get_azure_text_analytics_client(self) -> TextAnalyticsClient:
        if self._azure_text_analytics_client is None:
            try:
                logging.info("Creating Azure text analytics client")

                self._azure_text_analytics_client = TextAnalyticsClient(
                    endpoint=self.config.azure_cognitive_services_api_endpoint,
                    credential=AzureKeyCredential(
                        self.config.azure_cognitive_services_api_key
                    ),
                )

            except Exception as e:
                logging.error(f"Can't create Azure text analytics client: {e}")
                self._azure_text_analytics_client = None

        return self._azure_text_analytics_client

    def get_azure_immersive_reader_token(self) -> str:
        """
        Get the auth Token for the Immersive Reader UI component.
        This requires some setup, see:  https://docs.microsoft.com/en-us/azure/cognitive-services/immersive-reader/how-to-create-immersive-reader

        """
        clientId = self.config.azure_immersive_reader_client_id
        clientSecret = self.config.azure_immersive_reader_client_secret
        # AAD auth endpoint
        tenantId = self.config.azure_immersive_reader_tenant_id
        subdomain = self.config.azure_immersive_reader_subdomain

        resource = "https://cognitiveservices.azure.com/"
        oauthTokenUrl = f"https://login.windows.net/{tenantId}/oauth2/token"
        grantType = "client_credentials"

        try:
            headers = {"content-type": "application/x-www-form-urlencoded"}
            data = {
                "client_id": clientId,
                "client_secret": clientSecret,
                "resource": resource,
                "grant_type": grantType,
            }

            resp = requests.post(
                oauthTokenUrl,
                data=data,
                headers=headers,
            )
            jsonResp = resp.json()

            if "access_token" not in jsonResp:
                print(jsonResp)
                raise Exception(
                    "AAD Authentication error. Check your Immersive Reader access credentials",
                )

            token = jsonResp["access_token"]

            return {"token": token, "subdomain": subdomain}

        except Exception as e:
            message = f"Unable to acquire Azure AD token for Immersive Reader: {str(e)}"
            logging.error(message)
            raise Exception(message)

    def get_bing_custom_search_client(self) -> requests.Session:
        if self._bing_custom_search_client is None:
            try:
                logging.info("Creating Bing custom search client")

                # No python client library, using HTTP requests directly
                self._bing_custom_search_client = requests.Session()

                subscription_key = self.config.bing_custom_search_api_key
                custom_config_id = self.config.bing_custom_search_config_id

                self._bing_custom_search_client.headers.update(
                    {"Ocp-Apim-Subscription-Key": subscription_key}
                )
                self._bing_custom_search_client.params = {
                    "q": "",
                    "customConfig": custom_config_id,
                    "count": "3",
                    "offset": "0",
                    "mkt": "en-us",
                    "safesearch": "Off",
                }

            except Exception as e:
                logging.error(f"Can't create Bing custom search client: {e}")
                self._bing_custom_search_client = None

        return self._bing_custom_search_client

    def get_dictionary_client(self) -> requests.Session:
        if not self.config.mw_medical_dictionary_api_key:
            logging.warning("No medical dictionary API key configured")
            return None

        if self._dictionary_client is None:
            try:
                logging.info("Creating Dictionary client")

                self._dictionary_client = requests.Session()

            except Exception as e:
                logging.error(f"Can't create Dictionary client: {e}")
                self._dictionary_client = None

        return self._dictionary_client

    def configure_spacy_model(
        self,
        model_id="en_core_web_sm",
        force_reload=False,
        config: Dict[str, Dict[str, str]] = {},
    ) -> spacy.Language:
        """This gives central access to the spacy models that are installed / enabled in this platform.
        All the found summed extsions are installed and configured here upon first call.

        As the Language / Vocabs are shared, the returned Language should be considered a singleton.
        You may use the spacy pipeline concepts to enable/disable pipes for differen Analysis Configurations

        Args:
            model_id (str, optional): _description_. Defaults to "en_core_web_sm".

        Returns:
            spacy.Language: _description_
        """
        if self._spacy_models.get(model_id) and not force_reload:
            logging.info(f"spaCy model with '{model_id}' has already initialized. ")
            return self._spacy_models.get(model_id)
        else:
            try:
                logging.info(f"Loading spaCy model {model_id} ...")

                # TODO think about how we wanto do make this extensible and configurable
                logging.info(
                    f"Installing SumMed custom components on language model '{model_id}'..."
                )

                ####
                ##
                ## Import all the custom components, needed so we can register them with the pipeline
                ## TODO: Probably do this only once and on startup (?)

                ###
                pytextrank_module = import_module_by_name("pytextrank.biasedrank")
                analysis_module = import_module_by_name("summed.analysis")

                #### Loading the spaCy Language model...
                custom_config = config or {}
                model: spacy.Language = spacy.load(
                    model_id, exclude=["senter"], config=custom_config
                )

                # SumMed core extension, by definition start with "summed_"
                # TODO assert that all "core" components are installed
                summed_custom_components = [
                    name for name in model.factory_names if name[:7] == "summed_"
                ]

                # Senter should always be enabled
                # model.add_pipe("senter", after="parser")

                # TODO Review this: may be different per language, and some of the pipes should be inserted
                # in oder places (instead of appended)
                from scispacy.hyponym_detector import HyponymDetector
                from scispacy.custom_sentence_segmenter import pysbd_sentencizer
                from scispacy.custom_tokenizer import (
                    combined_rule_tokenizer,
                    combined_rule_prefixes,
                    remove_new_lines,
                )
                from scispacy.abbreviation import AbbreviationDetector

                model.tokenizer = combined_rule_tokenizer(model)
                model.add_pipe("pysbd_sentencizer", first=True)
                model.add_pipe(
                    "abbreviation_detector", config={"make_serializable": True}
                )
                model.add_pipe(
                    "hyponym_detector", last=True, config={"extended": False}
                )

                model.add_pipe("biasedtextrank", config={})
                model.add_pipe("summed_translation")
                model.add_pipe("summed_health_entities")
                model.add_pipe("summed_summarizer")
                model.add_pipe("summed_gpt3_summarizer")

                model.add_pipe("summed_trusted_search")
                model.add_pipe("summed_trust_score")
                model.add_pipe("summed_glossary_lookup")
                model.add_pipe("summed_preprocess_text")

                # Cache for later use
                self._spacy_models[model_id] = model

            except Exception as e:
                logging.error(f"Can't load spaCy model {model_id}: {e}")

        return self._spacy_models.get(model_id, None)

    def discover_plugins(self, force_reload=False):
        """Load all the plugins in the platform

        Args:
            force_reload (bool, optional): Force re-loading of modules/components. Defaults to False.
        """
        NotImplementedError()

    def __init__(self, config: PlatformConfig = None, **kwargs):
        try:
            super().__init__(config=config or PlatformConfig(), **kwargs)
            logging.info(
                f"SumMed Platform instance created - '{version('summed')}' {self.config.environment}"
            )

        except Exception as e:
            logging.error(f"Invalid platform configuration: {e}")
            raise e

    class Config:
        # see https://pydantic-docs.helpmanual.io/usage/model_config/
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
