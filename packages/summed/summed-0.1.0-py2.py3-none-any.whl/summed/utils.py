import importlib
import logging
import mimetypes
import os
import re
from gettext import translation
from types import ModuleType

import io
from playwright.sync_api import sync_playwright
from PIL import Image

import asyncio

# Fiy problem with on windows event loop
# see: https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
import sys

if "win32" in sys.platform:
    # Windows specific event-loop policy & cmd
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


def collapse_whitespace(text: str) -> str:
    """Collapse whitespace (linebreaks, tabs, space, ...) in a string.

    Args:
        text (str):raw text

    Returns:
        str: normalized text: single newline, no tabs, no spaces
    """
    result = text
    result = re.sub("\r+", "\n", result)
    result = re.sub("\n+", "\n", result)
    result = re.sub(" +", " ", result)
    result = re.sub("\t+", " ", result)

    return result


def create_filename_from_url(url: str, add_timpestamp: bool = True) -> str:
    pass


def create_thumbnail_from_url(url: str, size: tuple = (128, 128)) -> bytes:
    """Create thumbnail from webpage by URL.
    
    WARNING: Before using this function, please use 'playwright install' command to install browsers.

    Args:
        url (str): URL of webpage
        size (tuple, optional): Size of thumbnail. Defaults to (128,128).

    Returns:
        bytes: thumbnail image as StringIO object (ready to be written to a file)
        None: if no thumbnail could be created
    """
    bytes_buffer = None
    try:
        # Create screenshot
        with sync_playwright() as p:
            browser = p.webkit.launch()
            page = browser.new_page()
            page.goto(url)
            bytes_buffer = page.screenshot(type="jpeg")
            browser.close()
    except Exception as ex:
        logging.error(f"Could not create thumbnail from '{url}': {ex} ")

    if bytes_buffer:
        # Create thumbnail
        thumbnail = Image.open(io.BytesIO(bytes_buffer))
        # thumbnail.save("page_test.jpg", "JPEG") # for testing, save original image to a file !!!
        thumbnail.thumbnail(size)

        # Create virtual file-like object
        saved_thumbnail = io.BytesIO()
        # Save thumbnail to virtual file-like object
        thumbnail.save(saved_thumbnail, "JPEG")
        # Return thumbnail image as StringIO object (it will be ready to be written to a file)
        return saved_thumbnail.getvalue()
    else:
        return None


# "pytextrank.biasedrank"
def import_module_by_name(module: str) -> ModuleType:
    return importlib.import_module(module)


# def import_all_from_module(module: str) -> list:
#     """Import recursivly all children from a module, much like "from my.module import *"
#     ( children MUST be listed in module "__all__")

#     Args:
#         module (str): The module name e.g. "summed.analysis"

#     Returns:
#         list: ModuleTypes of all direct children of the module
#     """
#     module = import_module_by_name(module)

#     component_modules = [
#         import_all_from_module(f"{module}.{component}")
#         for component in module.__all__
#         if component
#     ]
