import logging
import time

import pytesseract
import requests
from PIL import Image

logger = logging.getLogger(__name__)


def process_image_data(req_data):
    logger.info("Received request to convert image to text")
    file_url = req_data['url']
    text_to_return = ""
    response = None
    try:
        response = requests.get(file_url, stream=True)
    except Exception as e:
        logging.exception(e)

    if response is not None:
        fileName = './tempFile.png'
        with open(fileName, "wb") as f:
            f.write(response.content)
            f.close()
        startTime = time.time()
        logger.info("extracting text from document")
        img = Image.open(fileName)
        logger.info(img)
        text_to_return = pytesseract.image_to_string(img)
        logger.info("completed extracting text from file in : " + str((time.time() - startTime) * 1000) + "ms")

    return text_to_return
