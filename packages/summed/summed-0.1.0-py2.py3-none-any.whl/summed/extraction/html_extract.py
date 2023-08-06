import logging
import re

from bs4 import BeautifulSoup
from boilerpy3 import extractors
from boilerpy3.document import TextDocument

from summed.data import Document, FileInfo
from summed.summed_platform import SumMedPlatform
from summed.utils import collapse_whitespace

from summed.extraction import ExtractorPluginSpec, IExtractorStrategy


# @ExtractorPluginSpec.summed_extractor_factory
# def html_extractor_factory(platform: SumMedPlatform, **kwargs) -> IExtractorStrategy:
#     logging.info(f"Creating HTML extractor")
#     return HTMLStrategy(platform, **kwargs)


class HTMLStrategy(IExtractorStrategy):
    def can_handle(self, source_file: FileInfo) -> bool:
        return re.match("text/html", source_file.content_type)

    def extract_from_bytes(self, data: bytes, document: Document) -> Document:
        raw_html = data.decode("utf-8")  # TODO: handle different encodings

        # Example
        # source_url = "https://www.breastcancer.org/research-news/risk-reducing-effects-of-arimidex-last-years"

        #
        # Step 1.: Use BeautifulSoup to parse and preprocess the HTML.
        # see: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        #
        soup = BeautifulSoup(raw_html, "lxml")  # html.parser
        #  Remove heading tags
        [tag.decompose() for tag in soup.select("h1, h2, h3, h4, h5, h6")]
        # Remove <script> tags
        [tag.decompose() for tag in soup.select("script")]

        # Retrieve some metadata from the HTML
        document.title = soup.find("title") and soup.find("title").text
        author_tag = soup.find("meta", {"name": "author"}) or {}
        document.author = author_tag.get("content", "unknown")
        # copy all "meta" attributes over to document.metadata
        tags = []
        for tag in soup.find_all("meta"):
            k = tag.get("name") or tag.get("property")
            v = tag.get("content") or tag.text
            if k and v:
                tags.append({k: v})
        document.metadata["html_meta"] = tags

        # Get the full HTML text from the preprocessed
        preprocessed_html = str(soup)

        #
        # Step 2.: Extract text from the preprocessed HTML, using boilerpy3.
        # see: https://github.com/jmriebold/BoilerPy3
        #
        html_extractor = (
            extractors.KeepEverythingExtractor()
        )  # extractors.CanolaExtractor()  #
        text_doc: TextDocument = html_extractor.get_doc(preprocessed_html)

        # Get text and collapse whitespace
        document.text = collapse_whitespace(text_doc.content)

        return document
