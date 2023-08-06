#!/usr/bin/env python

"""SumMed setup script."""

###
### Recommended setup.py for Windows
###    - install chocolatey
###    - run "choco install pyenv-win"
###    - run "pyenv install 3.8.10"
###    - run "pyenv global 3.8.10"

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=8.0.3",
    "pydantic<1.9.0",  # 1.9.0 is breaking for spacy 3.2.1
    "requests>=2.26.0",
    "requests-file>=1.5.1",
    "python-dotenv>=0.19.2",
    "azure-core>=1.21.1",
    "azure-storage-blob>=12.9.0",
    "azure-ai-textanalytics>=5.1.0",
    "azure-ai-formrecognizer>=3.1.2",
    "bs4>=0.0.1",
    "spacy[lookups]>=3.2.1",
    "pytextrank>=3.2.2",
    "en_core_web_sm",
    "ru_core_news_sm",
    "pt_core_news_sm",
    "de_core_news_sm",
    "xx_sent_ud_sm",
    "openai>=0.16.0",
    "boilerpy3>=1.0.6",
    "pluggy>=0.13.1",
    "charset-normalizer>=2.0.12",
    "lxml>=4.5.0",
    "scispacy>=0.5.0",
    "pikepdf>=5.1.3",
    "streamlit>=1.10.0",
    "fastapi>=0.85.1",
    "uvicorn>=0.19.0"
    #  "en_core_sci_sm", TODO get it to work with our Python 3.8 version ?
]

test_requirements = [
    "pytest>=3",
    "pytest-bdd>=5.0.0",
    "pytest-datadir>=1.3.1",
    "pytest-benchmark>=3.4.1",
]

setup(
    author="SumMed Team",
    author_email="hello@summed.org",
    # TODO because of scispacy dependency,
    # we need to use 3.8. See https://github.com/allenai/scispacy/issues/291#issuecomment-771076466
    # Problem is nmslib 2.1.1. which won't build easily on Windows, and has no published binary bindings for python 3.9 (yet)
    python_requires=">=3.8, <3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    description="SumMed empowers patients and caregivers to better understand medical information",
    entry_points={
        "console_scripts": [
            "summed=summed.cli:main",
        ],
        # see https://spacy.io/usage/saving-loading
        # TODO fill in the rest and check if necessary, as we load the components dynamically via imports on platform init (e.g. before creating Language model instances)
        # "spacy_factories": [
        #     "summed_translation = summed.analysis.translation:create_translation",
        #     "summed_health_entities = summed.analysis.health_entities:create_health_entities",
        #     "summed_summarizer = summed.analysis.summarizer:create_summed_summarizer",
        #     "summed_gpt3_summarizer",
        #     "summed_trusted_search",
        #     "summed_trust_score",
        #     "summed_glossary_lookup",
        # ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="summed",
    name="summed",
    packages=find_packages(include=["summed", "summed.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/whatchacallit/summed",
    version="0.1.0",  # Important: need to bump
    zip_safe=False,
)
