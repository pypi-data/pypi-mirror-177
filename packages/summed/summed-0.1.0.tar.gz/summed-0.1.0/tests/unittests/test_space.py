#!/usr/bin/env python


"""
Testing basic file management functions.
SumMed expects all input files to be in one "space". Users authenticate to their space and can list, upload, replace, and delete files.
The Space is usually backed by Azure Blob Storage, but should be able to be used with other storage options.

"""

import os, pytest, base64, logging, re, json
from pathlib import Path


from summed.data import DocumentSource, FileInfo
from summed.summed_platform import SumMedPlatform
from summed.user import User
from summed.space import ISpace, Space
from summed.extractor import Extractor
from summed.analyzer import Analyzer
from summed.analysis.configurations import (
    CREATE_ABSTRACTIVE_SUMMARY,
    CREATE_SUMMARY,
    PROFILE_FULL,
)


def test_empty_space_that_should_have_no_files(platform):
    space = Space(platform=platform, name="empty_space")
    files = space.list_files()
    assert len(files) == 0


@pytest.mark.needs_internet
def test_upload_same_filename_from_different_sources_should_work(
    user: User, space: ISpace
):

    my_space = space

    content = base64.b64encode(b"hello world")

    # No files -> 1 file
    assert len(my_space.list_files()) == 0
    info1 = my_space.upload(DocumentSource(filename="sample.txt", data=content))
    assert len(my_space.list_files()) == 1

    # re-upload the same file again -> 2 files (new filename)
    info2 = my_space.upload(
        DocumentSource(filename="sample.txt", data=content), overwrite=False
    )
    assert len(my_space.list_files()) == 2
    assert (
        info2.filename != info1.filename
    ), "Filename should be different when uploading using an existing filename, and overwrite=False"

    info3 = my_space.upload(
        DocumentSource(filename="sample.txt", data=content), overwrite=True
    )
    assert len(my_space.list_files()) == 2
    assert (
        info1.filename == info3.filename
    ), "Filename should be SAME when uploading using an existing filename, and overwrite=True"

    # add another file -> 3 files. Use an existing  filename and overwrite, so no additional filename is generated
    info3 = my_space.upload(
        DocumentSource(
            url="https://en.wikipedia.org/wiki/Oncology",
            filename=info2.filename,
            content_type="application/html",
        ),
        overwrite=True,
    )
    assert len(my_space.list_files()) == 2
    assert (
        info3.filename == info2.filename
    ), "Filenames should stay the SAME when re-uploading a file, and overwrite=True"


def test_download_file_after_upload_should_work(space: ISpace):

    content = base64.b64encode(b"hello world")

    my_space = space
    assert len(my_space.list_files()) == 0

    # upload a file with some embedded data (base64 encoded).
    file1: FileInfo = my_space.upload(
        DocumentSource(filename="sample.txt", data=content)
    )
    assert len(my_space.list_files()) == 1

    assert file1.filename == "sample.txt"
    assert file1.size == 11
    assert file1.last_modified is not None
    assert file1.metadata is not None

    # download the file and check the data
    assert my_space.download(file1) == b"hello world"

    # convenience: we only need the filename, as it is unique within a space
    assert my_space.download(file1.filename) == b"hello world"


def test_delete_file(space: ISpace):
    content = base64.b64encode(b"hello world")

    my_space = space
    source = DocumentSource(filename="sample.txt", data=content)

    # upload a file with some embedded data (base64 encoded).
    file1: FileInfo = my_space.upload(source)
    assert len(my_space.list_files()) == 1

    # just make sure delete works
    my_space.delete_file(file1)

    assert len(my_space.list_files()) == 0

    """ upload again """
    file2 = my_space.upload(source)
    assert len(my_space.list_files()) == 1


def test_list_files(space: ISpace):

    my_space = space

    source1 = DocumentSource(
        filename="sample1.txt", data=base64.b64encode(b"hello world 1")
    )
    source2 = DocumentSource(
        filename="sample2.txt", data=base64.b64encode(b"hello world 2")
    )
    source3 = DocumentSource(
        filename="sample3.txt", data=base64.b64encode(b"hello world 3")
    )
    source4 = DocumentSource(
        filename="sample4.txt", data=base64.b64encode(b"hello world 4")
    )
    source4_duplicate = DocumentSource(
        filename="sample4.txt",
        data=base64.b64encode(b"hello world 4 with different content"),
    )

    my_space.upload(source1)
    assert len(my_space.list_files()) == 1
    assert my_space.list_files()[0].filename == "sample1.txt"

    my_space.upload(source2)
    assert len(my_space.list_files()) == 2
    assert my_space.list_files()[1].filename == "sample2.txt"

    my_space.upload(source3)
    my_space.upload(source4)

    assert len(my_space.list_files()) == 4
    assert my_space.list_files()[3].filename == "sample4.txt"

    # Upload with existing filename ("sample4.txt") should create a new file named "sample4_<timestamp>.txt"
    my_space.upload(source4_duplicate)
    assert len(my_space.list_files()) == 5
    assert re.match(r"sample4_\d+\.txt", my_space.list_files()[4].filename, re.I)


def test_download_file_that_does_not_exist_should_fail(space: ISpace):
    my_space = space
    with pytest.raises(Exception):
        my_space.download("sample.txt")


@pytest.mark.needs_internet
def test_upload_and_download_from_different_sources(space: ISpace):
    my_space = space

    # embedd base64 encoded data in the source
    embedded_source = DocumentSource(
        filename="sample.txt", data=base64.b64encode(b"hello world")
    )
    # dummy https URL as a source (see httpbin.org for details)
    http_source = DocumentSource(
        filename="sample_request.json",
        url="https://httpbin.org/get?hello=world",
        content_type="application/json",
    )

    # upload
    my_space.upload(embedded_source)
    my_space.upload(http_source)

    # Download again and verify
    data = my_space.download("sample.txt")
    assert data == b"hello world"

    data = my_space.download("sample_request.json")
    assert data is not None
    assert len(data) > 0

    d = dict(json.loads(data))
    assert d["args"]["hello"] == "world"


def test_setting_and_guessing_content_type(space: ISpace):
    my_space = space

    # Explicitly provide a content type (text/plain)
    text_file_with_content_type = DocumentSource(
        filename="sample.txt",
        data=base64.b64encode(b"hello world"),
        content_type="text/plain",
    )
    result = my_space.upload(text_file_with_content_type)
    assert result.content_type == "text/plain"

    # Don't provide a content type, make us guess by the filename (application/json)
    text_file_without_content_type = DocumentSource(
        filename="sample.json",
        data=base64.b64encode(b"{'hello': 'world'}"),
    )
    result = my_space.upload(text_file_without_content_type)
    assert result.content_type == "application/json"

    # Mismatch between filename/extension and indicated content type (application/json)
    file_with_mismatched_content_type = DocumentSource(
        filename="sample.html",
        data=base64.b64encode(b"<html></html>"),
        content_type="application/json",
    )
    result = my_space.upload(file_with_mismatched_content_type)
    assert result.content_type == "application/json"

    # Default should be application/octet-stream
    result = my_space.upload(
        DocumentSource(
            filename="sample.unknown", data=base64.b64encode(b"<html></html>")
        )
    )
    assert result.content_type == "application/octet-stream"

    # ... but we can override it by providing a common file extension
    result = my_space.upload(
        DocumentSource(filename="sample.html", data=base64.b64encode(b"<html></html>"))
    )
    assert result.content_type == "text/html"

    # Try some url sources
    result = my_space.upload("https://en.wikipedia.org/wiki/Breast_cancer")
    assert result.content_type == "text/html"
    assert result.filename == "Breast_cancer.html"

    # Trailing slash (also follows redirect)
    result = my_space.upload("https://en.wikipedia.org/")
    assert result.content_type == "text/html"
    # FIXME should probably  be 'en_wikipedia_org.html'
    assert result.filename == "en_wikipedia.org"


def test_upload_download_local_file(space: Space, shared_datadir):
    my_space = space

    p = Path(shared_datadir / "simple_test.txt")
    original_content = p.read_bytes()

    # upload from local file uri (file://...)
    small_local_file = DocumentSource(
        filename="sample.txt", url=str(p.as_uri()), content_type="text/plain"
    )
    # upload
    my_space.upload(small_local_file)

    # Download again and verify
    data = my_space.download("sample.txt")
    assert data == original_content


def test_get_public_url(space: Space):
    my_space = space

    my_file = my_space.upload("https://en.wikipedia.org/wiki/Breast_cancer")
    public_url = my_space.get_public_url(my_file.filename)

    assert "Breast_cancer.html" in public_url


@pytest.mark.needs_internet
def test_save_document(
    platform: SumMedPlatform, space: ISpace
):
    extractor = Extractor(platform)

    # Upload from url to the space
    url = "https://www.californiaprotons.com/breast-cancer/prevention-causes-risk-factors/"
    source_file = space.upload(url)
    
    # Extract to a new document
    document = extractor.extract(source_file)

    # Do something with the document to fill in the fields
    # analyzer = Analyzer(platform)
    # document = analyzer.analyze (document, CREATE_SUMMARY)
    # document = analyzer.analyze(document, CREATE_ABSTRACTIVE_SUMMARY)
    # document = analyzer.analyze(document, PROFILE_FULL)

    # Upload from the document to json-file in the space (json cannot contain bytearray fields):
    document = space.save_document(document)
    assert document.document_file
    assert (document.source_file.filename + "_SumMed_Document_" in document.document_file.filename) and (
        ".json" in document.document_file.filename
    )

    document = space.save_document(document, filename="my_doc")
    assert "my_doc" in document.document_file.filename


def test_find_documents(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):
    extractor = Extractor(platform)

    # Save some documents to the space
    my_path = Path(shared_datadir / "web_article_breast_cancer_prevention_en.html")
    space.save_document(extractor.extract(space.upload(my_path)))
    
    my_path = Path(shared_datadir / "simple_html_article.html")
    space.save_document(extractor.extract(space.upload(my_path)))
    
    my_path = Path(shared_datadir / "normas-de-orientação-oncogenética.pdf")
    space.save_document(extractor.extract(space.upload(my_path)))
    
    # Find all documents
    doc_list = space.find_documents(max=2)
    assert doc_list[0].document_file
    assert len(doc_list) == 2
    # Find all document filenames
    file_list = space.find_documents(query="filename")
    assert len(file_list) == 3


def test_delete_document_files(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):
    extractor = Extractor(platform)

    space.delete_all_files()

    # Save some documents to the space
    my_path = Path(shared_datadir / "web_article_breast_cancer_prevention_en.html")
    space.save_document(extractor.extract(space.upload(my_path)))
    
    my_path = Path(shared_datadir / "simple_html_article.html")
    space.save_document(extractor.extract(space.upload(my_path)))
    
    my_path = Path(shared_datadir / "normas-de-orientação-oncogenética.pdf")
    space.save_document(extractor.extract(space.upload(my_path)))
    
    # Get the list of all documents
    doc_list = space.find_documents()
    assert len(doc_list) == 3

    # Delete document by filename
    assert space.delete_document_files(doc_list[0].document_file.filename)
    assert len(space.find_documents()) == 2
    # Chek delettion of non-existing or wrong name file
    assert not space.delete_document_files(doc_list[0].document_file.filename)

    # Delete document by FileInfo object
    assert space.delete_document_files(doc_list[1].document_file)
    assert len(space.find_documents()) == 1

    # Delete document by Document object, with source option
    # (in this case, thumbnail file and source file also can be deleted)
    assert space.delete_document_files(doc_list[2], source=True)
    assert len(space.find_documents()) == 0
    # Chek that thumbnail is also deleted
    assert not space.is_existfile(doc_list[2].thumbnail_file.filename)
    # Chek that source_file is also deleted
    assert not space.is_existfile(doc_list[2].source_file.filename)


def test_load_document(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):
    extractor = Extractor(platform)

    # Save some document to our 'space'
    my_path = Path(shared_datadir / "web_article_breast_cancer_prevention_en.html")
    document = extractor.extract(space.upload(my_path))
    document = space.save_document(document)

    # Load the document by filename
    document1 = space.load_document(document.document_file.filename)
    assert document.text == document1.text

    # Load the document by FileInfo object
    document1 = space.load_document(document.document_file)
    assert document.text == document1.text

    # Load the document by Document object
    document1 = space.load_document(document)
    assert document.text == document1.text

