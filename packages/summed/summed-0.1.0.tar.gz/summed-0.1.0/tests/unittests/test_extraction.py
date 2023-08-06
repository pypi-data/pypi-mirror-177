#!/usr/bin/env python


"""
Testing basic extraction features 

"""

import os, pytest, base64, logging, re, json
from numpy import extract
from pathlib import Path


from summed.data import Document, DocumentSource, FileInfo
from summed.summed_platform import SumMedPlatform
from summed.user import User, IUser
from summed.space import ISpace, Space
from summed.extractor import Extractor


def test_extract_from_plain_text_file(
    platform: SumMedPlatform,
    space: ISpace,
    shared_datadir,
):

    p = Path(shared_datadir / "simple_test.txt")

    original_content = p.read_bytes()
    info = space.upload(p)

    extractor = Extractor(platform)
    result: Document = extractor.extract(info)

    assert result.source_file.filename == "simple_test.txt"
    assert result.source_file.content_type == "text/plain"

    assert result.text == original_content.decode("utf-8")


def test_extract_from_html_page(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):

    info = space.upload(Path(shared_datadir / "simple_html_article.html"))

    extractor = Extractor(platform)
    result: Document = extractor.extract(info)

    assert result.source_file.filename == "simple_html_article.html"
    assert result.source_file.content_type == "text/html"

    assert result.title == "Simple HTML Article"
    assert "This is a simple HTML article." in result.text


@pytest.mark.needs_internet
def test_extract_from_html_page_public_url(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):
    # Use convenience method
    info = space.upload(
        "https://www.breastcancer.org/research-news/risk-reducing-effects-of-arimidex-last-years"
    )

    extractor = Extractor(platform)
    result: Document = extractor.extract(info)

    assert re.match(
        r"^risk_reducing_effects_of_arimidex_last_years.*\.html$",
        result.source_file.filename,
    )
    assert result.source_file.content_type == "text/html"

    assert (
        result.title
        == "Risk-Reducing Effects of Arimidex for High-Risk Postmenopausal Women Last Years After Treatment Stops"
    )
    assert "Postmenopausal women at high risk for breast cancer" in result.text


@pytest.mark.needs_internet
def test_extract_from_pdf_file(platform: SumMedPlatform, space: ISpace, shared_datadir):

    info = space.upload(Path(shared_datadir / "simple_test.pdf"))

    extractor = Extractor(platform)

    # Our setup can handle pdfs, via form_recognizer
    assert platform.has_form_recognizer
    assert extractor.can_handle(info)

    document: Document = extractor.extract(info)

    assert document.source_file.filename == "simple_test.pdf"
    assert document.source_file.content_type == "application/pdf"
    # assert document.title == "Simple PDF Article"


def test_extract_from_docx_file(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):

    info = space.upload(Path(shared_datadir / "summed_trial_text_04_08_22.docx"))

    extractor = Extractor(platform)
    # Our setup can handle pdfs, via form_recognizer
    assert platform.has_form_recognizer
    assert extractor.can_handle(info)

    document: Document = extractor.extract(info)

    assert document.source_file.filename == "summed_trial_text_04_08_22.docx"
    assert (
        document.source_file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert document.text


def test_extract_from_portuguese_pdf_file(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):

    info = space.upload(Path(shared_datadir / "normas-de-orientação-oncogenética.pdf"))

    extractor = Extractor(platform)

    # Our setup can handle pdfs, via form_recognizer
    assert platform.has_form_recognizer
    assert extractor.can_handle(info)

    document: Document = extractor.extract(info)

    # assert document.source_file.filename == "normas-de-orientação-oncogenética.pdf"
    assert document.source_file.content_type == "application/pdf"
    assert document.text

    # assert document.title == "Simple PDF Article"


def test_extract_from_image_files(
    platform: SumMedPlatform, space: ISpace, shared_datadir
):
    info = space.upload(Path(shared_datadir / "simple_test.jpg"))

    extractor = Extractor(platform)

    # Our setup can handle pdfs, via form_recognizer
    assert extractor.can_handle(info)

    document: Document = extractor.extract(info)

    assert document.source_file.filename == "simple_test.jpg"
    assert document.source_file.content_type == "image/jpeg"

    assert document.text


def test_extract_from_wikipedia(platform: SumMedPlatform, user: User):
    pass


def test_extract_from_audio_file(platform: SumMedPlatform, user: User):
    pass


def test_extract_common_metadata_detection(platform: SumMedPlatform, user: User):
    pass
