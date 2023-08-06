import logging, collections, requests
from openai import Search
from spacy.language import Language, Doc

from summed.summed_platform import SumMedPlatform
from summed.data import Document, NamedEntity, SearchResult


@Language.component("summed_trusted_search")
def create_summed_trusted_search(doc, use_abstractive_summary: bool = True):
    """Run a web/Knowledge-base search for related content. Use the available information for highly targeted and highly relevant search on trustworthy sources only.
    Currently, this uses a Microsoft Bing Custom Search V7.0 API with a curated list of trusted sources (cancer.org, mayoclinic.org, etc.).)

    Args:
        doc (_type_): _description_
    """

    def perform_trusted_web_search(
        platform: SumMedPlatform, doc: Doc, document: Document
    ):
        """Performs a web search on a query to find highly related documents from trustworthy sites.

        Returns:
            List[Searchresult]: A list of related resources from trusted sites.
        """
        logging.info(f"Performing trusted search...")
        search_results = []
        if not platform.has_trusted_search:
            logging.warning(f"Trusted search is unavailable, skipping")
            return []

        if not Doc.has_extension("summed_summarizer") or not doc._.get(
            "summed_summarizer"
        ):
            logging.warning(
                "The summed_summarizer extension component is not available/run. Please make sure it runs before the trusted search."
            )
            return []

        base_url = platform.config.bing_custom_search_api_base_url

        # TODO: Build a smart query, based on the summary or other doc information
        if use_abstractive_summary and document.abstractive_summary:
            search_query = " ".join(document.abstractive_summary)
        else:
            search_query = " ".join(document.summary)

        search_query = search_query[:100]  # cut off at 100 chars

        search_client: requests.Session = platform.get_bing_custom_search_client()

        # see: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/reference/query-parameters
        response = search_client.get(
            base_url,
            params={
                **search_client.params,
                **{"q": search_query, "count": "10", "mkt": f"{document.language}"},
            },
        )
        response.raise_for_status()
        pages_results = dict(response.json())

        # pages_results['webPages']['value'] => (name, url, displayUrl, language, snippet)
        pages = [
            SearchResult(
                last_accessed=d["dateLastCrawled"],
                image=d["openGraphImage"]["contentUrl"]
                if d.get("openGraphImage")
                else None,
                name=d["name"],
                url=d["url"],
                snippet=d["snippet"],
            )
            for d in pages_results["webPages"]["value"]
        ]

        # Store in document
        document.search_results = pages

        return pages

    # Register the extension
    if not Doc.has_extension("summed_trusted_search"):
        Doc.set_extension("summed_trusted_search", default=[], force=True)

    # Register the function
    doc._.summed_trusted_search = (
        lambda platform, doc, document: perform_trusted_web_search(
            platform, doc, document
        )
    )

    return doc
