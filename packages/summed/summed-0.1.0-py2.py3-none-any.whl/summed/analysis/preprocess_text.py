from hashlib import new
import logging, collections
import re
from spacy.language import Language, Doc

from summed.summed_platform import SumMedPlatform
from summed.data import Document, NamedEntity, TrustScore
import summed.utils as utils


# def is_valid_sentence(sentence, doc):

#     if len(sentence) > 200:
#         return False
#     if len(sentence) < 30:
#         return False

#     return True


# def preprocess_document_text(
#     platform: SumMedPlatform,
#     doc: Doc,
#     document: Document,
#     collapse_whitespace: bool = True,
#     sentence_filtering: bool = True,
# ):
#     """ """
#     logging.info(f"Preprocessing text...")

#     # TODO: Implement the actually scoring algorithms
#     new_text = document.text

#     # TODO: this is not preprocess but "filtering" / post-process
#     if sentence_filtering and document.sentences:
#         logging.info("Preprocessing based on sentences")
#         new_text = "".join(
#             [
#                 sentence
#                 for sentence in document.sentences
#                 if is_valid_sentence(sentence, doc)
#             ]
#         )

#     # Remove based on re patterns
#     # RULE: Newlines between words turn into a dot
#     # new_text = re.sub(r"([A-Za-z])\n+([A-Za-z])", r"\1.\2", new_text)

#     # collapse whitespace
#     if collapse_whitespace:
#         new_text = utils.collapse_whitespace(new_text)

#     # RULE: Replace all newlines between words with a single space
#     new_text = re.sub(r"(\S)\n+(\S)", r"\1 \2", new_text)

#     # RULE: Replace "\n " with a single space
#     new_text = re.sub(r"(\S)\n (\S)", r"\1 \2", new_text)

#     # collapse whitespace again
#     if collapse_whitespace:
#         new_text = utils.collapse_whitespace(new_text)

#     document.text = new_text.strip()

#     return new_text


# @Language.factory(
#     "summed_preprocess_text",
#     default_config={"collapse_whitespace": True, "sentence_filtering": True},
# )
# class SummedPreprocessText:
#     def __init__(
#         self,
#         nlp: Language,
#         namse: str,
#         collapse_whitespace: bool,
#         sentence_filtering: bool,
#     ):
#         self.nlp = nlp
#         self.collapse_whitespace = collapse_whitespace
#         self.sentence_filtering = sentence_filtering

#     def __call__(self, doc: Doc, **kwargs) -> Doc:
#         if not Doc.has_extension("summed_preprocess_text"):
#             Doc.set_extension("summed_preprocess_text", default={}, force=True)

#         # Register the function
#         doc._.summed_preprocess_text = (
#             lambda platform, doc, document: preprocess_document_text(
#                 platform,
#                 doc,
#                 document,
#                 collapse_whitepace=self.collapse_whitespace,
#                 sentence_filtering=self.sentence_filtering,
#             )
#         )


@Language.component("summed_preprocess_text")
def create_summed_preprocessor(doc, collapse_whitespace: bool = True):
    """Preprocess document.text"""

    def preprocess_document_text(
        platform: SumMedPlatform, doc: Doc, document: Document
    ):
        """ """
        logging.info(f"Preprocessing text...")

        # TODO: Implement the actually scoring algorithms
        new_text = document.text

        # Remove based on re patterns
        # RULE: Newlines between words turn into a dot
        # new_text = re.sub(r"([A-Za-z])\n+([A-Za-z])", r"\1.\2", new_text)

        # collapse whitespace
        if collapse_whitespace:
            new_text = utils.collapse_whitespace(new_text)

        # replace "-\n(\w)" with "\1"
        new_text = re.sub(r"-\n+(\w)", r"\1", new_text)

        # RULE: Replace all newlines between words with a single space
        # new_text = re.sub(r"(\S)\n+(\S)", r"\1 \2", new_text)
        new_text = re.sub(r"\.\n", ". ", new_text)

        # RULE: Replace "\n " with a single space
        # new_text = re.sub(r"(\S)\n (\S)", r"\1 \2", new_text)
        new_text = re.sub(r"(\S)\n (\S)", r"\1 \2", new_text)

        # collapse whitespace again
        if collapse_whitespace:
            new_text = utils.collapse_whitespace(new_text)

        new_text = re.sub(r"\n", " ", new_text)

        # FIXME: remove "Advertisement " from demo docs
        new_text = re.sub(r"Advertisement ", "", new_text)
        new_text = re.sub(r"([^\.]) The", r"\1\. The", new_text)
        new_text = re.sub(r"About Arimidex Arimidex", "Arimidex", new_text)

        document.text = new_text.strip()

        return document.text

    if not Doc.has_extension("summed_preprocess_text"):
        Doc.set_extension("summed_preprocess_text", default={}, force=True)

    # Register the function
    doc._.summed_preprocess_text = (
        lambda platform, doc, document: preprocess_document_text(
            platform, doc, document
        )
    )

    return doc
