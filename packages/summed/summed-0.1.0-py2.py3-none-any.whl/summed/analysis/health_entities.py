# Stateless variant, e.g. no config
# This uses "defered" mode, e.g. the registered extension is a callable which gets called with platform/ doc after the nlp callS
# see: https://docs.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python
# sample code: https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-textanalytics_5.1.0/sdk/textanalytics/azure-ai-textanalytics/samples/sample_analyze_healthcare_entities.py

import logging, collections
from spacy.language import Language, Doc

from summed.summed_platform import SumMedPlatform
from summed.data import Document, NamedEntity

from azure.ai.textanalytics import HealthcareEntity, HealthcareEntityCategory


@Language.component("summed_health_entities")
def create_summed_health_entities(doc):
    """Look up health entities in the document, e.g using Azure Text Analytics for Health.

    TODO: This does not use spaCy at all at the moment but just calls an API.
    We need to review if / how good we could leverage specialized public spaCy models and components for this - e.g.:

    medspaCy: A toolkit for clinical NLP with spaCy.
    - https://spacy.io/universe/project/medspacy
    - https://github.com/medspacy/medspacy


    scispaCy:A full spaCy pipeline and models for scientific/biomedical documents
    - https://spacy.io/universe/project/scispacy
    - https://allenai.github.io/scispacy/

    Note: the spaCy models are not available as a component, but would need to be managed by the  SumMed platform.:

    """

    def _get_health_entities(platform: SumMedPlatform, doc: Doc, document: Document):
        """Lookup and group healthcare entities using Azure Text Analytics for Health.

        Returns:
            List[NamedEntity]: List of detected healthcare entities, ordered by frequency
        """

        entities = []
        logging.info(f"Getting results from Azure Text Analytics for Health")

        if not platform.has_text_analytics_for_health:
            logging.warn(f"Azure Text Aalytics fro Health is unavailable, skipping")
            return []

        client = platform.get_azure_text_analytics_client()
        documents = [doc.text]

        poller = client.begin_analyze_healthcare_entities(documents)
        result = poller.result()

        docs = [doc for doc in result if not doc.is_error]

        categories_of_interest = [
            HealthcareEntityCategory.AGE,
            HealthcareEntityCategory.BODY_STRUCTURE,
            HealthcareEntityCategory.CARE_ENVIRONMENT,
            HealthcareEntityCategory.DIAGNOSIS,
            HealthcareEntityCategory.DIRECTION,
            HealthcareEntityCategory.DOSAGE,
            HealthcareEntityCategory.EXAMINATION_NAME,
            HealthcareEntityCategory.FAMILY_RELATION,
            HealthcareEntityCategory.FREQUENCY,
            HealthcareEntityCategory.GENDER,
            HealthcareEntityCategory.GENE_OR_PROTEIN,
            HealthcareEntityCategory.HEALTHCARE_PROFESSION,
            HealthcareEntityCategory.MEDICATION_CLASS,
            HealthcareEntityCategory.MEDICATION_FORM,
            HealthcareEntityCategory.MEDICATION_NAME,
            HealthcareEntityCategory.MEDICATION_ROUTE,
            HealthcareEntityCategory.SYMPTOM_OR_SIGN,
            HealthcareEntityCategory.TREATMENT_NAME,
            HealthcareEntityCategory.VARIANT,
        ]

        for idx, doc in enumerate(docs):
            for entity in doc.entities:

                # print("Entity: {}".format(entity.text))
                # print("...Normalized Text: {}".format(entity.normalized_text))
                # print("...Category: {}".format(entity.category))
                # print("...Subcategory: {}".format(entity.subcategory))
                # print("...Offset: {}".format(entity.offset))
                # print("...Confidence score: {}".format(entity.confidence_score))

                if entity.category in categories_of_interest:
                    entities.append(
                        (
                            entity.normalized_text or entity.text,
                            entity.category,
                        )
                    )

            cnt = collections.Counter(entities)

        entities = [
            NamedEntity(text=ent_data[0], label=ent_data[1], count=ent_count)
            for ent_data, ent_count in reversed(
                sorted(cnt.items(), key=lambda item: item[1])
            )
        ]

        # Store in document
        document.health_entities = entities

        return entities

    # regsiter the extension
    if not Doc.has_extension("summed_health_entities"):
        Doc.set_extension("summed_health_entities", default=[], force=True)

    # Register the function
    doc._.summed_health_entities = lambda platform, doc, document: _get_health_entities(
        platform, doc, document
    )

    return doc
