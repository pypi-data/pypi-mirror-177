import os, time, logging, pytest
from pathlib import Path

from dotenv import load_dotenv


from azure.storage.blob import BlobServiceClient
from summed.data import PlatformConfig, Document, DocumentSource, FileInfo


from summed.summed_platform import SumMedPlatform
from summed.user import User
from summed.space import Space
from summed.extractor import Extractor


def pytest_generate_tests(metafunc):

    # Create a container for Azurite for the first run
    # Load environment variables from .env file (if present)
    # This would contain secrets that are not meant to be commited to git
    load_dotenv(".env")

    # Load environment variables from .env.testing
    load_dotenv(".env.testing")

    # Set log levels
    # see: https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-logging#set-logging-levels
    logger = logging.getLogger("azure.core")
    logger.setLevel(logging.WARN)

    try:

        blob_service_client = BlobServiceClient.from_connection_string(
            os.environ.get("SUMMED_AZURE_STORAGE_CONNECTION_STRING")
        )
    except Exception as e:
        logging.error(f"Failed to connect to blob service : {e}.")
        logging.error(
            f"Please set the SUMMED_AZURE_STORAGE_CONNECTION_STRING environment variable."
        )
        logging.error(
            "Also make sure Azurite (Azure Storage emulator) is running. See README.md for more info."
        )
        raise (e)

    #
    # Name of the storage container
    container_name = os.environ.get("SUMMED_AZURE_STORAGE_CONTAINER")
    try:
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            logging.warning(f"Container {container_name} does not exist. Creating...")
            container_client.create_container()

        retry_counter = 0
        while not container_client.exists():
            if retry_counter > 5:
                raise Exception(
                    "Failed to create container after quite some retries, giving up now...."
                )
            else:
                logging.warning(f"...still trying ...")
                time.sleep(2)
                continue

    except Exception as e:
        logging.error(f"Failed to create storage container: {e}")
        logging.error(
            "Also make sure Azurite (Azure Storage emulator) is running. See README.md for more info."
        )

        raise e


## Shared fictures ##
"""Unit test package for summed."""


@pytest.fixture(scope="module")
def platform():
    # setup platform
    platform = SumMedPlatform(PlatformConfig(environment="testing"))

    # run the underlying test ("yield" injects the platform into the test function)
    yield platform

    # teardown


@pytest.fixture(scope="function")
def user(platform: SumMedPlatform):

    # SETUP
    logging.info("SETUP")
    user = User(platform=platform, name="unittest user")
    user.authenticate()

    # RUN test
    # injects the user into the test function
    yield user

    # TEARDOWN
    logging.info("TEARDOWN")

    user.logout()


@pytest.fixture(scope="function")
def space(platform: SumMedPlatform):

    space = Space(platform=platform, name="unittest space")

    yield space

    if space.exists():
        space.delete()


@pytest.fixture(scope="function")
def document_simple_file_en(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "simple_test_en.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_simple_file_de(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "simple_test_de.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_simple_file_pt(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "simple_test_pt.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_simple_file_ru(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "simple_test_ru.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_breast_cancer_en(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "breast_cancer_en.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_sentencing_basic_test_en(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "sentencing_basic_test_en.html"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_news_article_cancer_en(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "news_article_cancer_en.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_news_article_cancer_pt(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "news_article_cancer_pt.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_news_article_cancer_de(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "news_article_cancer_de.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_news_article_cancer_ru(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(Path(shared_datadir / "news_article_cancer_ru.txt"))
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def document_pdf_portuguese_oncogenetica(platform: SumMedPlatform, shared_datadir):
    space = Space(platform)
    file_info = space.upload(
        Path(shared_datadir / "normas-de-orientação-oncogenética.pdf")
    )
    document: Document = Extractor(platform).extract(file_info)

    yield document

    space.delete_file(file_info)


@pytest.fixture(scope="function")
def documents_news_article_cancer(
    document_news_article_cancer_en,
    document_news_article_cancer_pt,
    document_news_article_cancer_de,
    document_news_article_cancer_ru,
):
    yield {
        "en": document_news_article_cancer_en,
        "de": document_news_article_cancer_de,
        "pt": document_news_article_cancer_pt,
        "ru": document_news_article_cancer_ru,
    }
