import io
from pathlib import Path

import requests

from ExtractDoc import extract_text_from_doc
from ExtractPdf import extract_from_pdf
from config import config


def convert_to_text(file_url):
    text_to_return=""
    if "doc" in file_url or "docx" in file_url:
        if "http" in file_url or "https" in file_url:
            response = requests.get(file_url, stream=True)
            fileName = file_url.split("/")[-1]
            with open(fileName, "wb") as f:
                f.write(response.content)
                f.close()
            text_to_return = extract_text_from_doc(fileName)
            Path(fileName).rename(config.PROCESSED_FILE_PATH+fileName)
        else:
            text_to_return = extract_text_from_doc(config.FILE_PATH + file_url)
    elif "pdf" in file_url:
        if "http" in file_url or "https" in file_url:
            response = requests.get(file_url)
            pdf_content = io.BytesIO(response.content)
            text_to_return = extract_from_pdf(pdf_content)
            with open(config.PROCESSED_FILE_PATH+file_url.split("/")[-1], "wb") as f:
                f.write(response.content)
                f.close()
        else:
            pdfFileObj = open(config.FILE_PATH+file_url, 'rb')
            text_to_return = extract_from_pdf(pdfFileObj)
            pdfFileObj.close()

    return text_to_return
