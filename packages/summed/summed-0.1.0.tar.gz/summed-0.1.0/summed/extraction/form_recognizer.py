from io import BytesIO
import logging
import re


from summed.data import Document, FileInfo
from summed.extraction import IExtractorStrategy
from summed.summed_platform import SumMedPlatform

import pikepdf


from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import (
    DocumentAnalysisClient,
    AnalyzedDocument,
    AnalyzeResult,
)


class FormRecognizerStrategy(IExtractorStrategy):
    def __init__(self, platform: SumMedPlatform):
        super().__init__(platform)

    def can_handle(self, source_file: FileInfo) -> bool:
        if self.platform.has_form_recognizer:
            return re.match("application/pdf", source_file.content_type)

        return False

    def extract_from_bytes(self, data: bytes, document: Document) -> Document:
        endpoint = self.platform.config.azure_form_recognizer_api_endpoint
        api_key = self.platform.config.azure_form_recognizer_api_key

        # see docs: https://pypi.org/project/azure-ai-formrecognizer/3.2.0b3/

        model_id = "prebuilt-read"

        # https://pypi.org/project/azure-ai-formrecognizer/
        # TODO: support different form_recognizer models -
        # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/formrecognizer/azure-ai-formrecognizer/samples/v3.1/sample_recognize_content.py

        form_recognizer_client = DocumentAnalysisClient(
            endpoint, AzureKeyCredential(api_key)
        )

        poller = form_recognizer_client.begin_analyze_document(
            model=model_id, document=data
        )

        # TODO async ? Takes anything upward of 2 secs
        form_pages: AnalyzeResult = poller.result()

        document.text = form_pages.content
        # TODO this just takes the detected language of the first detected text (which is often so short;) )
        # document.language = form_pages.languages[0].locale     , but... we have another way:
        
        # Determine the most commonly used language in the form has been recognized
        list_of_locales = []
        # a list of the count of text spans in each language
        list_of_counts_of_spans = []
        
        for language in form_pages.languages:
            if language.locale not in list_of_locales:
                # Add the locale to the list of locales
                list_of_locales.append(language.locale)
                list_of_counts_of_spans.append(len(language.spans))
            else:
                # Increment the count of spans for the locale
                index = list_of_locales.index(language.locale)
                list_of_counts_of_spans[index] += len(language.spans)
        # Find the index of the locale with the most counts
        document.language = list_of_locales[list_of_counts_of_spans.index(max(list_of_counts_of_spans))]

        # TODO For PDFs, find a way to extract metadata like title (if available)
        # Use pikepdf ? https://pikepdf.readthedocs.io/en/latest/
        # document.title = meta['dc:title']

        all_text_lines = []

        # for idx, content in enumerate(form_pages.pages):
        #     logging.info(
        #         f"Recognizing content from page #{idx+1} width={content.width} , height={content.height}, unit={content.unit} "
        #     )
        #     # for table_idx, table in enumerate(content.tables):
        #     #    pass
        #     for line_idx, line in enumerate(content.lines):
        #         all_text_lines.append(line.text)

        # document.text = " ".join(all_text_lines)

        return document
