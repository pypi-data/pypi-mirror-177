import logging, collections
from spacy.language import Language, Doc

from summed.summed_platform import SumMedPlatform
from summed.data import Document, NamedEntity, TrustScore


@Language.component("summed_trust_score")
def create_summed_trust_score(doc):
    """Calculate the trust score for the document.
    This is a weighted score of different metrics that are calculated.

    TODO:Good practice would be coming up something that will support implementation of
    the HAX Guidelines -
    see:
    https://www.microsoft.com/en-us/haxtoolkit/toolkit-overview/

    HAX Library:
    https://www.microsoft.com/en-us/haxtoolkit/library/
    https://www.microsoft.com/en-us/haxtoolkit/library/?content_type%5B1%5D=pattern&taxonomy_product-category%5B0%5D=62&taxonomy_application-type%5B0%5D=56&taxonomy_application-type%5B%5D=59

    """

    def calculate_trust_scores(platform: SumMedPlatform, doc: Doc, document: Document):
        """Calculates the confidence and "trust" indicator scores for the document.
        Uses data, metadata and hard-coded rules to calculate the trust score.

        Returns:
            TrustScore: calculated scores and confidence
        """
        logging.info(f"Calculating trust score...")

        # TODO: Implement the actually scoring algorithms
        score = {
            "language_confidence": 0.0,
            # 0 no statistical model - 1 domain-specific model with high performance
            "model_confidence": 0.0,
            # 0 no domain detected - 1 domain detected (e.g. 'oncology') and explicity supported
            "domain_confidence": 0.0,
            # 0 no source indication - 1 from a trusted, verified source
            "source_confidence": 0.0,
            # 0 known problems with extraction of data - 1 clear and clean text extraction
            "extraction_confidence": 0.0,
            # 0 no/problematic analysis - 1 everything went smoothly
            "analysis_confidence": 0.0,
        }

        document.trust_score = TrustScore(**score)
        return score

    if not Doc.has_extension("summed_trust_score"):
        Doc.set_extension("summed_trust_score", default={}, force=True)

    # Register the function
    doc._.summed_trust_score = lambda platform, doc, document: calculate_trust_scores(
        platform, doc, document
    )

    return doc
