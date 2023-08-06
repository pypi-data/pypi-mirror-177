from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from pydantic import (  # TODO FileUrl supported by pydantic>1.9.0 but not yet in spacy 3.2.1
    BaseModel,
    BaseSettings,
    Field,
    HttpUrl,
    validator,
)


class DocumentSource(BaseModel):
    """
      Specify the (original) source of the document. Currently, this can be one of the following things:
    - a HTTP URL to a remote resource, potentially with a sasToken (e.g. https://myaccount.blob.core.windows.net/mycontainer/myfile.txt?sastoken)
    - a local file path (as a file:// uri)
    - an internal combination of (blob storage) containerName + filename
    - data bytes directly embedded (base64 encoded)
    """

    type: str = "file"

    container: Optional[str] = None
    data: Optional[bytes] = None
    url: Optional[
        Union[HttpUrl, str]
    ] = None  # TODO FileUrl supported by pydantic>1.9.0 but not yet in spacy 3.2.1

    filename: Optional[str]
    sasToken: Optional[str] = None
    content_type: Optional[str] = None

    @validator("filename", "container", "data", "url", pre=True)
    def validate(cls, v, values):
        if (
            len([i for i in ["filename", "container", "data", "url"] if i in values])
            == 0
        ):
            raise ValueError(
                "Either filename, container, data or url field must be provided"
            )

        return v


class FileInfo(BaseModel):
    """
    Holds information about a file in a blob storage container
    """

    filename: str
    size: Optional[int]
    last_modified: Optional[datetime]
    metadata: Optional[dict] = None
    content_type: Optional[str] = None

    class Config:
        json_encoders = {
            bytearray: lambda v: list(
                v
            ),  # convert bytearray to list (json cannot contain bytearray fields)
            datetime: lambda v: v.isoformat(),  # convert datetime to iso string
        }


class TrustScore(BaseModel):
    # 0 unknown/unsupported - 1 fully supported language (e.g. english)
    language_confidence: Optional[float]
    # 0 no statistical model - 1 domain-specific model with high performance
    model_confidence: Optional[float]
    # 0 no domain detected - 1 domain detected (e.g. 'oncology') and explicity supported
    domain_confidence: Optional[float]
    # 0 no source indication - 1 from a trusted, verified source
    source_confidence: Optional[float]
    # 0 known problems with extraction of data - 1 clear and clean text extraction
    extraction_confidence: Optional[float]
    # 0 no/problematic analysis - 1 everything went smoothly
    analysis_confidence: Optional[float]


class NamedEntity(BaseModel):
    text: str
    label: str
    count: Optional[int]
    # fuzzy_frequency: Optional[float] = 0.0


class TermExplanation(BaseModel):
    term: str
    explanation: Optional[List[str]] = None
    source: Optional[str] = None


class GlossaryContainer(BaseModel):
    glossary: Optional[Dict[str, TermExplanation]] = None
    filename: Optional[str] = "SumMed_glossary.json"


class SearchResult(BaseModel):
    url: Optional[str]
    name: Optional[str]
    snippet: Optional[str]
    image: Optional[str]
    last_accssed: Optional[str]
    source: Optional[str]


class Document(BaseModel):
    """Holds all the data around a SumMed document, like references to source and file in storage,
    extracted text, metadata, and summary data.
    This is the main object that gets "enriched" while processing, possibly in an iterative fashion

    """

    version: Optional[str] = "1.0.0"
    source_file: FileInfo
    # file where the document is stored
    document_file: Optional[FileInfo] = None
    # file where thumbnail of the source file is stored
    thumbnail_file: Optional[FileInfo] = None

    # Language is important for selecting the right models etc.
    # We should try to use language-specific models (or fairly language agnostic algorithms), where available.
    # We also may want to translate the text conent of this document at some point, as some features may only be supported in certain languages (like english).
    language: Optional[str] = None
    original_language: Optional[str] = None
    # original_document: Optional[Document] = None

    title: Optional[str] = None
    author: Optional[str] = "unknown"

    # Text and metadata extracted from the source file and will be modified during processing
    text: Optional[str] = None
    metadata: Optional[dict] = {}

    document_type: Optional[str] = "unkown"
    medical_domain: Optional[str] = "unknown"

    sentences: Optional[List[str]] = None
    sentences_lemma: Optional[List[str]] = None

    summary: Optional[List[str]] = None
    summary_lemma: Optional[List[str]] = None

    entities: Optional[List[NamedEntity]] = None
    health_entities: Optional[List[NamedEntity]] = None

    abstractive_summary: Optional[str] = None

    search_results: Optional[List[SearchResult]] = None

    trust_score: Optional[TrustScore] = None

    glossary: Optional[Dict[str, TermExplanation]] = None

    translations: Optional[Dict[str, Dict[str, str]]] = None

    class Config:
        json_encoders = {
            bytearray: lambda v: v.hex(), # convert bytearray to hex (json cannot contain bytearray fields),
            # to reverse use bytearray.fromhex(<hexstr>)
            # datetime: lambda v: v.isoformat(),  # convert datetime to iso string - Is it possible to implement without this conversion?
            # Because it creates serious difficulties for saving/loading the document in space.
        }


class AnalysisConfig(BaseSettings):
    """Configuration settings for Analyzer"""

    def __mod__(self, other):
        # Mod operator is used to change pipeline_config ia "A % {"component": "disable"}""}""
        # Semantic: keep all keys from self.pipeline_config, and whatever is in self.enable
        if isinstance(other, dict):
            r = self.copy(deep=True)
            for component in set(
                r.enable + list(r.pipeline_config.keys()) + list(other.keys())
            ):
                r.pipeline_config[component] = {
                    **self.pipeline_config.get(component, {}),
                    **other.get(component, {}),
                }
            return r
        else:
            raise NotImplementedError(
                f"Mod operator not implemented for '{type(other)}'"
            )

    def __add__(self, other):
        # union of two lists, remove double entries (like a set), but keep order of first list (unlike a set)
        enable_union = list(dict.fromkeys(self.enable + other.enable))
        disable_union = list(dict.fromkeys(self.disable + other.disable))

        r = self.copy(deep=True)
        r.enable = enable_union
        r.disable = disable_union
        r.pipeline_config = {**self.pipeline_config, **other.pipeline_config}

        return r

    pipeline_package: Optional[str]  # = "en_core_web_sm"
    pipeline: Optional[List[str]] = None

    # ONLY these "pipe" components of the pipeline will be enabled. Entries ignored if not part of the pipeline.
    # Should be a subset of the pipeline of the spaCy Language model
    enable: Optional[List[str]] = []

    # ENSURE that these are disabled. (overrides 'enable' field. Entries ignored if not part of the pipeline)
    disable: Optional[List[str]] = []

    # enabled pipeline components can receive custom configuration properties from here.
    # the config can hold data for currently disabled or unknonw pipe names, it's simply ignored
    # see: https://spacy.io/api#architecture-pipeline for config for build-in spaCy components
    pipeline_config: Optional[Dict[str, Dict[str, Any]]] = {
        # see: https://spacy.io/api/textcategorizer#config
        "biasedtextrank": {},
        "summed_summarizer": {"num_sentences": 5, "preserve_order": True},
        "summed_health_entities": {},
        "summed_trusted_search": {},
        "summed_glossary_lookup": {},
        "summed_translations": {},
        "summed_trust_score": {},
        "summed_gpt3_summarizer": {},
    }


class PlatformConfig(BaseSettings):
    """
    Holds configuration for a SumMed platform.
    A platform instance represents a particular configuration of the system, holding credentials, activated extensions and other settings.

    Note that this leveages Pydantic support for environment vars / .env:
    - by default, all envionment vars must start with "SUMMED_" prefix
    - not case sensitive
    - e.g. PlatformConfig.azure_storage_container == os.environ['SUMMED_AZURE_STORAGE_CONTAINER']

    Creating a PlatformConfig will pull the settings from current os.environ and the parameters specified.
    A few settings are "required" e.g. (Storage connection), so constructor will fail if not specified via environment variables or parameters.
    """

    environment: str = Field("", env="ENVIRONMENT")

    # Azure Blob storage. This is required - e.g. if not set, creation of this config will fail
    #
    azure_storage_connection_string: str
    azure_storage_container: str

    # Azure Translation Service
    # see:https://docs.microsoft.com/en-us/azure/cognitive-services/translator/
    azure_translation_api_key: str = None
    azure_translation_api_endpoint: str = None
    azure_translation_api_location: str = None

    # Azure Cognitive Services for language
    # see: https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/
    # https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/text-analytics-for-health/quickstart?pivots=programming-language-python
    azure_cognitive_services_api_key: str = None
    azure_cognitive_services_api_endpoint: str = None

    #
    # Azure Form Recognizer
    # see: https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/how-to-guides/try-sdk-rest-api?pivots=programming-language-python
    #
    azure_form_recognizer_api_key: str = None
    azure_form_recognizer_api_endpoint: str = None
    azure_form_recognizer_api_location: str = None

    # Azure Immersive Reader
    # (provide IR token to frontend, ignored in "headless"/CLI mode,
    # as IR is a frontend component)
    # This requires some setup, see:  https://docs.microsoft.com/en-us/azure/cognitive-services/immersive-reader/how-to-create-immersive-reader
    azure_immersive_reader_region: str = None
    azure_immersive_reader_client_id: str = None
    azure_immersive_reader_client_secret: str = None
    azure_immersive_reader_tenant_id: str = None
    azure_immersive_reader_subdomain: str = None

    # Bing Custom (internet) search
    # see:
    bing_custom_search_api_base_url: str = None
    bing_custom_search_api_key: str = None
    bing_custom_search_config_id: str = None

    # Merriam Webster Medical Dictionary API
    # see:
    mw_medical_dictionary_api_key: str = None
    mw_medical_dictionary_base_url: str = None

    # OpenAI API Key to access GPT-3 API
    # OpenAI for GPT-3 - see https://beta.openai.com/
    openai_api_key: str = None

    class Config:
        # see https://pydantic-docs.helpmanual.io/usage/settings/
        env_prefix = "SUMMED_"

        # secrets_dir = '/var/run'
