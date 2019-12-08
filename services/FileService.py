import os

import requests
import urllib

from ExtractDoc import extract_text_from_doc
from ExtractPdf import extract_from_pdf


def convert_to_text(file_url):
    text_to_return=""
    if "doc" in file_url or "docx" in file_url:
        text_to_return = extract_text_from_doc(file_url)
    elif "pdf" in file_url:
        file = requests.get(file_url)
        text_to_return = extract_from_pdf(file)

    return text_to_return
