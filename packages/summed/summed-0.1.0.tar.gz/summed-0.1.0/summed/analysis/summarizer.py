import logging
from summed.summed_platform import SumMedPlatform
from summed.data import Document
from spacy.language import Language, Doc

from pytextrank.base import BaseTextRank
from pytextrank.biasedrank import BiasedTextRank


# See: https://spacy.io/usage/processing-pipelines#custom-components-simple


@Language.component(
    "summed_summarizer",
)
def create_summed_summarizer(
    doc: Doc,
    num_sentences: int = 5,
    limit_phrases: int = 64,
    preserve_order: bool = True,
):
    """Create an (extractive) Summary of the document.
    We use the pytextrank module which creats the "textrank" extension on the Doc object.
    see : https://derwen.ai/docs/ptr/ref/#basetextrank-class


    Args:
        doc (Doc): spacy Doc
        num_sentences (int, optional): Number of sentences to return. Defaults to 5.
        limit_phrases (int, optional): Max number . Defaults to 64.
        preserve_order (bool, optional): _description_. Defaults to True.
    """

    def summarizer(platform: SumMedPlatform, doc: Doc, document: Document):
        logging.info(f"Extractive summarization (num_sentences={num_sentences}) ...")

        if not doc.has_extension("textrank"):
            raise Exception(
                f"No 'textrank' extension data found. Make sure summarizer runs after the 'textrank' (or equal) pipeline component"
            )

        summary = []

        tr = doc._.textrank
        logging.info(f"Creating extractive summary...")

        # Biased TextRank
        # TODO make this configurable. Think: how can we guide the algorithm to get the best sentences.
        # paper: https://aclanthology.org/2020.coling-main.144.pdf
        if isinstance(tr, BiasedTextRank):
            focus_set = "breast cancer"
            logging.info(f"Biased text rank, changing focus={focus_set}...")
            tr.change_focus(focus=focus_set, bias=1.0, default_bias=0.0)

        ranked = tr.summary(
            limit_phrases=limit_phrases,
            limit_sentences=num_sentences,
            preserve_order=preserve_order,
        )
        summary = [str(sentence) for sentence in ranked]

        # TODO further filter e.g. too short / similiar sentences

        document.summary = summary

        return summary

    # This is globally enabled, when this component is loaded
    if not Doc.has_extension("summed_summarizer"):
        Doc.set_extension("summed_summarizer", default=[], force=True)

    # set summary
    doc._.summed_summarizer = lambda platform, doc, document: summarizer(
        platform, doc, document
    )

    return doc


# -------------------------------------
