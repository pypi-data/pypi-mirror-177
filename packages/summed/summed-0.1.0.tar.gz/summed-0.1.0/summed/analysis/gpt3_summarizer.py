import logging, collections
import os
import openai

from spacy.language import Language, Doc
from summed.data import Document

from summed.summed_platform import SumMedPlatform


# TODO:
# Learn about good prompt desing, filtering, length control etc.:
# https://beta.openai.com/docs/introduction/prompt-design-101
# https://help.openai.com/en/articles/5072518-controlling-the-length-of-completions
# https://beta.openai.com/docs/api-reference/completions/create


@Language.component("summed_gpt3_summarizer")
def create_summed_gpt3_summarizer(
    doc,
    engine: str = "text-davinci-002",
    prompt_prefix: str = "Summarize for a child:",  # TODO wors well: "Tell me what I should ask my doctor about this:"
    temperature: float = 0.0,
    max_tokens: int = 198,
    top_p: int = 1,
    n: int = 1,
    frequency_penalty: float = 0.4,
    presence_penalty: float = 0,
    use_summary_as_prompt: bool = True,
):
    """Use OpenAI GPT-3 to summarize and explain medical text."""

    def create_gpt3_abstractive_summary(
        platform: SumMedPlatform, doc: Doc, document: Document
    ):
        """
        Use GPT-3 to summarize the given document.
        This is a fairly generic way to call GPT-3 completion API


        Returns:
            _type_: _description_
        """
        logging.info(f"Looking up GPT3 abstractive summary...")

        if not platform.has_openai_gpt3:
            logging.warning(
                f"OpenAI features are not available, skipping GPT-3 abstractive summary"
            )
            return []

        openai.api_key = platform.config.openai_api_key

        # Use previously created summary as prompt, if inidcated and available. Full doc.text otherwise
        prompt = (
            "\n".join(document.summary)
            if (use_summary_as_prompt and document.summary)
            else doc.text
        )

        # TODO Limit total prompt  to a maximum number of tokens (max 2948 token), or the openai.Completion call will fail.
        # Simplest would be to just cut off longer text at the end.
        # see: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        # So the challenge is that total_prompt mus not exceed 2048 tokens, roughly 1500 words, but depending on language and text.

        total_prompt = f"{prompt_prefix}\n\n{prompt}".strip()

        response = openai.Completion.create(
            engine=engine,
            prompt=total_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            n=n,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        summary = [choice.text.strip() for choice in response.choices]

        # TODO do some error handling here, e.g. if the completion had some issues (length, promot etc)

        # TODO do some content filtering (see:

        # Just take a not of some parameters we used
        document.metadata["gpt3_engine"] = engine

        # Store abstractive summary in document
        document.abstractive_summary = summary

        return summary

    ###
    ### Entry point: Register as document extension, and register callback function
    ###

    # Register extension
    if not Doc.has_extension("summed_gpt3_summarizer"):
        Doc.set_extension("summed_gpt3_summarizer", default=[], force=True)

    # Register the function
    doc._.summed_gpt3_summarizer = (
        lambda platform, doc, document: create_gpt3_abstractive_summary(
            platform, doc, document
        )
    )

    return doc
