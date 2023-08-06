#!/usr/bin/env python

"""
Testing Thumbnails

"""
import io
from PIL import Image

from summed.utils import create_thumbnail_from_url

def test_simple_webpage_thumbnail():
    # Test brocken link
    bytes_buffer = create_thumbnail_from_url(
        "https://www.aaa-breastcancer.org/research-news/risk-reducing-effects-of-arimidex-last-years"
    )
    assert bytes_buffer is None

    # Test default size (128x128) thumbnail
    bytes_buffer1 = create_thumbnail_from_url(
        "https://www.breastcancer.org/research-news/risk-reducing-effects-of-arimidex-last-years"
    )
    if bytes_buffer1:
        # Save thumbnail to file (example1):
        #       with open("thumbnail_test1.jpg", "wb") as f1:
        #           f1.write(bytes_buffer1)
        thumbnail1 = Image.open(io.BytesIO(bytes_buffer1))
        # If necessary, we can to perform some manipulations with the image, then save it (example2):
        #       thumbnail1.save("thumbnail_test1.jpg", "JPEG") 
        assert 128 in thumbnail1.size
    
    # Test custom size (200x200) thumbnail
    bytes_buffer2 = create_thumbnail_from_url(
        "https://www.breastcancer.org/research-news/risk-reducing-effects-of-arimidex-last-years",
        size = (200,200)
    )
    if bytes_buffer2:
        thumbnail2 = Image.open(io.BytesIO(bytes_buffer2))
        assert 200 in thumbnail2.size
