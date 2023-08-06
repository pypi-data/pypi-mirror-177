import logging, collections
from spacy.language import Language, Doc

from summed.summed_platform import SumMedPlatform
from summed.data import Document, NamedEntity
from summed.translation import AzureTranslator


@Language.component("summed_translation")
def create_summed_translation(doc, target_lang: str = "en"):
    """Translate the document text to the target language.
    This modifies the content of the document in place, replacing e.g. the following fields/text values with translated versions:
    - document.title
    - document.text
    - document.sentences
    - document.glossary (term, explanation fields)
    - document.entities (text)
    - document.health_entities (text)
    - document.search_result (snippet)

    Other changes to document:
    - sets document.original_language and document.metadata["from_language"] (if not set already) - a string, e.g. "ru"
    - appends target_lang to document.metadata["to_language"] - a list of strings (e.g. ["en", "de"])

    Args:
        doc (_type_): The spacy doc object.
        target_lang (str, optional): Language to translate to. If it's the same as the current document language, nothing will happen. Defaults to "en".
    """

    def translate_document_fields(
        platform: SumMedPlatform, doc: Doc, document: Document
    ):
        """Translates the text portions of the document.

        Modifies the document in place!

        TODO:
        Currently needs Azure Translator - check Deepl ? Support multiple translators via configuration?


        Returns:
            Dict[str, Any]: Dictionary with field/property names of Document, mapped to the new, translated values
        """
        logging.info(f"Translationg document to {target_lang}...")

        # TODO probably should support multiple translator implementations via  platform (e.g. Azure, Deepl, ...)
        if not platform.has_translator:
            logging.error(f"No translator available on platform, skipping")
            return {}

        if doc.lang_ == target_lang:
            logging.warning(f"Language of doc is already '{target_lang}', skipping")
            return {}

        try:
            logging.info(f"Calling translation API...")

            ## TODO support multiple translators. probably via platform.get_translator_client().
            translator: AzureTranslator = AzureTranslator(platform)

            translation = {}
            translation["language"] = target_lang

            # TODO: fine-grained calls to translate fields may be very inefficient (API calls).
            # Find a way to do this in a single call.

            ## Translate text
            translated_text = translator.translate(doc.text, target_lang)
            translation["text"] = translated_text
            if document.title:
                translation["title"] = translator.translate(document.title, target_lang)

            if document.sentences:
                translation["sentences"] = translator.translate(
                    "\n\n".join(document.sentences), target_lang
                ).split("\n\n")

            if document.summary:
                translation["summary"] = translator.translate(
                    "\n\n".join(document.summary), target_lang
                ).split("\n\n")
            if document.abstractive_summary:
                translation["abstractive_summary"] = [
                    translator.translate(document.abstractive_summary[0], target_lang)
                ]

            if document.entities:
                entity_text_lines = "\n".join(
                    [entity.text for entity in document.entities]
                )
                entity_text_translated = translator.translate(
                    entity_text_lines, target_lang
                ).split("\n")
                translation["entities"] = []
                for entity, translated_text in zip(
                    document.entities, entity_text_translated
                ):
                    translated_entity = entity.copy()
                    translated_entity.text = translated_text
                    translation["entities"].append(translated_entity)

            if document.health_entities:
                entity_text_lines = "\n".join(
                    [entity.text for entity in document.health_entities]
                )
                entity_text_translated = translator.translate(
                    entity_text_lines, target_lang
                ).split("\n")
                translation["health_entities"] = []
                for entity, translated_text in zip(
                    document.health_entities, entity_text_translated
                ):
                    translated_entity = entity.copy()
                    translated_entity.text = translated_text
                    translation["health_entities"].append(translated_entity)

            if document.search_results:
                search_snippets = "\n\n".join(
                    [sr.snippet for sr in document.search_results]
                )
                search_snippets_translated = translator.translate(
                    search_snippets, target_lang
                ).split("\n\n")
                translation["search_results"] = []
                for search_result, translated_snippet in zip(
                    document.search_results, search_snippets_translated
                ):
                    translated_sr = search_result.copy()
                    translated_sr.snippet = translated_snippet
                    translation["search_results"].append(translated_sr)

        except Exception as e:
            logging.error(f"Failed to translate: {e}")
            return {}

        if translation:
            # If we haven't translated before, set the original language to the current language
            document.original_language = document.original_language or document.language
            document.metadata["translated_from"] = document.original_language

            # append this translation to the list to language codes (we could do multiple translation chains)
            document.metadata["translated_to"] = document.metadata.get(
                "translated_to", []
            )
            document.metadata["translated_to"].append(translation["language"])

            # Language of and text changed
            document.language = translation["language"]
            document.text = translation["text"]

            #
            # Overwrite these only if we have a translation
            #
            document.title = translation.get("title") or document.title

            document.sentences = translation.get("sentences") or document.sentences
            document.summary = translation.get("summary") or document.summary

            document.abstractive_summary = (
                translation.get("abstractive_summary") or document.abstractive_summary
            )
            document.entities = translation.get("entities") or document.entities
            document.health_entities = (
                translation.get("health_entities") or document.health_entities
            )
            document.search_results = (
                translation.get("search_results") or document.search_results
            )

        return translation

    ########

    if not Doc.has_extension("summed_translation"):
        Doc.set_extension("summed_translation", default={}, force=True)

    # 1. Check if all prerequisites are met (required components registered, info available, config valid...)

    # 2. Register the function, fixing the configuration options
    doc._.summed_translation = (
        lambda platform, doc, document: translate_document_fields(
            platform, doc, document
        )
    )

    return doc
