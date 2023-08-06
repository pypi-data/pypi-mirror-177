import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from dotenv import load_dotenv
from pydantic import BaseModel

from summed.analysis.configurations import (
    CALCULATE_TRUST_SCORE,
    CREATE_ABSTRACTIVE_SUMMARY,
    CREATE_SUMMARY,
    DETECT_ENTITIES,
    DETECT_HEALTH_ENTITIES,
    DETECT_SENTENCES,
    GLOSSARY_LOOKUP,
    TRUSTED_SEARCH,
)
from summed.analyzer import Analyzer
from summed.data import (
    AnalysisConfig,
    Document,
    DocumentSource,
    FileInfo,
    PlatformConfig,
    SearchResult,
    TermExplanation,
)
from summed.extractor import Extractor
from summed.summed_platform import SumMedPlatform
from summed.space import Space


class SumMedAPI(BaseModel):
    """A Facade as "public API" for the usage of the SumMed library"""

    platform: Optional[SumMedPlatform] = None
    space: Optional[Space] = None
    extractor: Optional[Extractor] = None
    analyzer: Optional[Analyzer] = None

    def __init__(self, **kwargs):
        """Initialize SumMed object"""
        super().__init__(**kwargs)
        config: PlatformConfig = kwargs.get("config", PlatformConfig())

        self.platform = SumMedPlatform(config)
        self.space = Space(self.platform)
        self.extractor = Extractor(self.platform)
        self.analyzer = Analyzer(self.platform)

    def upload(
        self, source: Union[DocumentSource, Path, str], overwrite: bool = False
    ) -> FileInfo:
        """Uploads a file to the current SumMed space"""
        return self.space.upload(source, overwrite=overwrite)

    def extract(self, file_info: FileInfo) -> DocumentSource:
        """Extracts text from a file"""
        return self.extractor.extract(file_info)

    def analyze(
        self,
        document: Document,
        config: Union[AnalysisConfig, Dict[str, AnalysisConfig]],
    ) -> Document:
        """Analyzes a document"""
        return self.analyzer.analyze(document, config)
