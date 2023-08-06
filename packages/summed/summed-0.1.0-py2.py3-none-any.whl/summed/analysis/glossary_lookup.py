import logging, collections, requests
from spacy.language import Language, Doc

from summed.summed_platform import SumMedPlatform
from summed.data import Document, NamedEntity, TermExplanation


@Language.component("summed_glossary_lookup")
def create_summed_glossary(doc, option1: str = None):
    def lookup_glossary_terms(platform: SumMedPlatform, doc: Doc, document: Document):
        """Lookup explanation for terms (words or small phrases), e.g. the keys in document.glossary.
        For each key/"term", we'll look if there is a corresponding entry in the glossary, and if it already has an explanation.
        If not, look it up via the medical dictionary API client that is configured on the platform.

        Returns:
            dict: Dict[str, TermExplanation]
        """
        logging.info(f"Looking up glossary term definitions...")
        glossary = document.glossary or {}

        for term, explanation in glossary.items():
            if not explanation or not explanation.explanation:
                base_url = platform.config.mw_medical_dictionary_base_url

                source = base_url
                
                api_key = platform.config.mw_medical_dictionary_api_key
                dictionary_client: requests.Session = platform.get_dictionary_client()
                try:
                    response = dictionary_client.get(
                        base_url + term + '?key=' + api_key
                        )
                    response.raise_for_status()
                    shortdef_list = response.json()[0]["shortdef"]
                    
                except Exception as e:
                    logging.error(f"Error during '{source}' call for term '{term}': {e}")
                    result = ["Failed to retrieve explanation"]
                    
                else:
                    if isinstance(shortdef_list, list):
                        result = shortdef_list
                    else:
                        result = [str(shortdef_list)]
                    logging.info(f"The following explanations were found in '{source}' for the term '{term}': {result}")

                glossary[term] = TermExplanation(
                    term=term, explanation=result, source=source
                )

        document.glossary = glossary
        return glossary

    # Register extennsion
    if not Doc.has_extension("summed_glossary_lookup"):
        Doc.set_extension("summed_glossary_lookup", default={}, force=True)

    # Register the function
    doc._.summed_glossary_lookup = (
        lambda platform, doc, document: lookup_glossary_terms(platform, doc, document)
    )

    return doc
