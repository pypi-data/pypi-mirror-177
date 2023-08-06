# streamlit_app.py
import base64
from cmath import exp
from io import BytesIO
from pathlib import Path
from matplotlib.image import thumbnail
from numpy import extract
import spacy
import streamlit as st
import spacy_streamlit
import streamlit.components.v1 as components

from traitlets import observe
from summed.data import Document, DocumentSource, FileInfo
from summed.analysis.configurations import (
    CREATE_ABSTRACTIVE_SUMMARY,
    DETECT_HEALTH_ENTITIES,
    PREPROCESS_TEXT,
    DETECT_SENTENCES,
    CREATE_SUMMARY,
    TRANSLATE_TEXT,
    TRUSTED_SEARCH,
    PROFILE_FULL,
)

from annotated_text import annotated_text
from summed.streamlit.summed_component import summed_component


from summed.summed_api import SumMedAPI
from PIL import Image
from summed.utils import create_thumbnail_from_url

# Import our custom components
# from summed.streamlit.summed_component import summed_component


from dotenv import load_dotenv

load_dotenv("../../.env")
load_dotenv("../../.env.testing")


# https://docs.streamlit.io/library/cheatsheet


# Theme and style
# main: '#1DA57A'
# light: '#2CDAA3',
# dark: '#178160',
# contrastText: '#fff',


st.set_page_config(
    page_title="SumMed - Better understand medical information",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://help.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# SumMed\n Better understand *medical* information",
    },
)


#
# summed object is cached by (user) name
#
@st.experimental_memo
def get_summed_api(name) -> SumMedAPI:
    summed = SumMedAPI(name=name)
    return summed


translate = False  # st.sidebar.checkbox("Translate into portuguese", False)

#
# Build the sidebar and returns a file_info object
#
def get_file_info() -> FileInfo:
    """Builds the sidebar, used to specify a source (file_info)"""

    file_info: FileInfo = None

    with st.sidebar:
        st.sidebar.image("../summed_logo.png")
        error_msg = ""

        st.subheader("Please provide your medical document")
        url = None
        file = None
        camera_image = None
        textarea = None
        audio_file = None

        # Radio selection of input type
        upload_from = st.radio(
            "I need to better understand this...",
            ["Web article", "File", "Photo", "Text", "Recording"],
            on_change=lambda: clear(),
        )
        "---"
        # empty slots here for layout, will displaye only one element, based on what is selected as upload_from radio
        element_source = st.empty()
        element_message = st.empty()

        with st.spinner(text="Uploading document..."):
            if upload_from == "Web article":
                url = element_source.text_input(
                    "",
                    placeholder="please give us a web adress (URL)",
                )
                st.caption(
                    url
                    or "e.g. https://www.breastcancer.org/research-news/risk-reducing-effects-of-arimidex-last-years"
                )

            if upload_from == "File":
                file = element_source.file_uploader("")

            if upload_from == "Photo":
                camera_image = element_source.camera_input("Take a picture")

            if upload_from == "Text":
                textarea = element_source.text_area("Provide some text here.")

            try:
                if file is not None:
                    # 'file' is a BytesIO file-like object, let's upload as base64 encoded data
                    file_info = summed.upload(
                        DocumentSource(
                            filename=f"{file.name}",
                            data=base64.b64encode(file.getvalue()),
                        ),
                        overwrite=True,
                    )
                elif url:
                    # 'url' is just a url string, summed (hopefully) figures out the rest from here
                    file_info = summed.upload(url)
                    thumbnail = Image.open(
                        BytesIO(create_thumbnail_from_url(url, (400, 300)))
                    )
                    st.image(thumbnail)

                elif textarea:
                    # 'textarea' is a string, manually entered
                    file_info = summed.upload(
                        DocumentSource(
                            filename="textarea.txt",
                            data=base64.b64encode(textarea.encode("utf-8")),
                        ),
                        overwrite=True,
                    )
                elif camera_image:
                    file_info = summed.upload(
                        DocumentSource(
                            filename="camera_photo.jpg",
                            data=base64.b64encode(textarea.encode("utf-8")),
                        ),
                        overwrite=True,
                    )
            except Exception as ex:
                error_msg = f"{ex}"
                file_info = None

        if error_msg:
            element_message.error(error_msg)

        return file_info


@st.experimental_memo(suppress_st_warning=True)
def extract_document(_file_info, cachekey) -> Document:
    with st.spinner("Extracting..."):

        if st.sidebar.button("Clear", help="Try something else", on_click=clear):
            st.experimental_rerun()

        document = summed.extract(_file_info)
        # st.session_state.document = document
        return document


@st.experimental_memo
def analyze_document(_document, _what, cachekey):
    # document = st.session_state.document
    try:
        doc = summed.analyze(_document, _what)
        # st.session_state.document = document
        return doc
    except Exception as ex:
        st.error(f"Problem: {ex}")


def clear():
    if "document" in st.session_state:
        del st.session_state.document
    if "file_info" in st.session_state:
        del st.session_state.file_info
    file_info = None
    document = None


def preprocess_document(document) -> Document:
    doc = analyze_document(document, PREPROCESS_TEXT, document.text)
    doc = analyze_document(doc, DETECT_SENTENCES, document.text)
    if doc.language != "en":
        doc = analyze_document(doc, TRANSLATE_TEXT["en"], document.text)

    return doc


def summarize_document(document) -> Document:
    # doc = analyze_document(document, CREATE_SUMMARY, document.summary)
    # doc = analyze_document(doc, CREATE_ABSTRACTIVE_SUMMARY, document.text)
    # doc = analyze_document(doc, DETECT_HEALTH_ENTITIES, document.text)
    # doc = analyze_document(doc, TRUSTED_SEARCH, document.text)
    # if translate:
    #     doc = analyze_document(doc, TRANSLATE_TEXT["pt"], document.text)
    doc = summed.analyze(document, PROFILE_FULL)
    return doc


def build_summary_page(document):

    element_title = st.empty()
    element_author = st.empty()
    element_tags = st.empty()

    # element_title.header(f"{document.title}")


#########
#
# Main flow starts here
#
#########

user_space = "streamlit_user"  # st.sidebar.selectbox("User", ["demo_user", "demo2"])

summed: SumMedAPI = get_summed_api(user_space)

# TODO cache this, or we'll keep uploading every single refresh
file_info: FileInfo = get_file_info()
document: Document = None

if not file_info:
    st.header("Welcome to SumMed")
    "We will help you better understand medical information.\nPlease provide input on the sidebar."
    "For an interactive demo how to use SumMed, please have a look at the following resources:\n"

    # st.video("https://vimeo.com/699518936/f1407a3d89")
    components.iframe(
        src="https://player.vimeo.com/video/699518936?h=f1407a3d89",
        width=640,
        height=564,
    )
else:
    document: Document = extract_document(file_info, file_info.filename)


if document:
    # build_summary_page(document)

    with st.spinner("Preprocessing..."):
        document = preprocess_document(document)

    with st.spinner("Creating Summary"):
        document = summarize_document(document)

    # show_toggle = st.radio("", ["Summary", "Original Text"], horizontal=True)

    summed_component(document=document)

    # if document.summary:
    #     # st.header("Summary")
    #     col_left, col_right = st.columns(2)
    #     # annotated_text((t, f"key insight", "#f0f0f0"))

    #     st.markdown(
    #         f"I read the text for you, it's **{len (document.text)}** characters and about **{len (document.sentences)}** sentences."
    #     )

    #     with col_left:
    #         # st.markdown(f"{summary_string}")
    #         language = (
    #             document.original_language if document.original_language else "english"
    #         )
    #         # summed_textarea_component(
    #         #     key="info_extraction",
    #         #     title=f"Thanks for showing me this <b>{language}</b> web article about <b>breast cancer</b>",
    #         #     subtitle=f"The text was readable",
    #         #     body=f"The document is titled <b>'{document.title}'</b> and was written by <b>{document.author}</b>.<br><br> I read <b>{len (document.text)}</b> characters and about <b>{len (document.sentences)}</b> sentences for you.<br><br>I can't verify the accuracy of your source, so be careful.<br/>It's best to talk to your doctor about this.",
    #         #     link="img/summed_owl.png",
    #         # )

    #         summary_string = (
    #             "<li>" + "<p></li><li>".join(document.summary[:3]) + "</li>"
    #         )
    #         summary_string = summary_string.replace(
    #             "example",
    #             "<span style='background: cyan; border-radius:20%; height: 5px; width: 5px;'>example</span>",
    #         )
    #         st.markdown(f"Here're a few key points from the text")
    #         st.markdown(summary_string, True)
    #     # summed_textarea_component(
    #     #     key="info_summary",
    #     #     title=f"Here a few key points from the text",
    #     #     subtitle="I think I can help here...",
    #     #     body=f"{summary_string}",
    #     #     link="medication",
    #     # )

    #     with col_right:
    #         abstractive_summary = "\n".join(
    #             document.abstractive_summary
    #             or [
    #                 "Sorry, I couldn't find the right words. Please speak to your doctor."
    #             ]
    #         )
    #         st.markdown(f"A summary about this diagnosis")
    #         st.markdown(document.abstractive_summary[0], True)
    #         # summed_textarea_component(
    #         #     key="info_abstractive_summary",
    #         #     title=f"What is this about?",
    #         #     subtitle="This is more like a guess",
    #         #     body=f"{abstractive_summary}",
    #         #     link="summarize",
    #         # )

    #     if document.health_entities:
    #         key_concepts = ""
    #         for x in enumerate(document.health_entities[:10]):
    #             e = x[1]
    #             if e.label in [
    #                 "Diagnosis",
    #                 "MedicationName",
    #                 "MedicationClass",
    #                 "GeneOrProtein",
    #                 "ExaminationName",
    #             ]:
    #                 key_concepts += f"<li>{e.text} <small>({e.label})</small></li>"

    #         # summed_component(
    #         #     key="info_key_concepts",
    #         #     title=f"Key medical topics mentioned in the text",
    #         #     subtitle="I'm confident I can help you",
    #         #     body=f"{key_concepts}",
    #         #     link="category",
    #         # )

    #     related_search = "Sorry, I could not find anything closely related"
    #     if document.search_results:
    #         related_search = ""
    #         for x in enumerate(document.search_results[:3]):
    #             s = x[1]
    #             related_search += f"<p><img target='_top' src='{s.image or 'img/summed_owl.png'}' width='32px'></img> <a href='{s.url}'>{s.name}</a><br><small>{s.snippet}</small></p>"
    #     # summed_textarea_component(
    #     #     key="info_related_search",
    #     #     title=f"Additional information from trusted sources",
    #     #     subtitle="I'm confident I can help you",
    #     #     body=f"{related_search}",
    #     #     link="savedsearch",
    #     # )

    st.json(document.dict(), expanded=False)
