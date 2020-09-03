from pathlib import Path

import requests
import os.path
import time
import logging

from werkzeug.datastructures import FileStorage

from CustomException.CustomException import CustomWebException
from services.cvProcessService.ExtractDoc import extract_text_from_doc
from services.cvProcessService.ExtractPdf import extract_from_pdf
from config import config

logger = logging.getLogger(__name__)


def convert_to_text(file_url):
    text_to_return = ""
    if "doc" in file_url or "docx" in file_url:
        if "http" in file_url or "https" in file_url:
            startTime = time.time()
            logger.info("downloading file: " + file_url)
            try:
                response = requests.get(file_url, stream=True)
            except Exception as e:
                logging.exception(e)
                raise CustomWebException("Failed to fetch file", e.code)
            if response:
                logging.info("completed downloading file in : ", str((time.time() - startTime) * 1000) + "ms")
                fileName = file_url.split("/")[-1]
                with open(fileName, "wb") as f:
                    f.write(response.content)
                    f.close()
                startTime = time.time()
                logger.info("extracting text from document")
                text_to_return = extract_text_from_doc(fileName)
                logger.info("completed extracting text from file in : " + str((time.time() - startTime) * 1000) + "ms")
                Path(fileName).rename(config.PROCESSED_FILE_PATH + fileName)
                logger.info("save file, filepath:" + (config.PROCESSED_FILE_PATH + fileName))
        else:
            text_to_return = extract_text_from_doc(config.FILE_PATH + file_url)
    elif "pdf" in file_url:
        if "http" in file_url or "https" in file_url:
            startTime = time.time()
            logger.info("downloading file: " + file_url)
            try:
                response = requests.get(file_url)
            except Exception as e:
                logging.exception(e)
                raise CustomWebException("Failed to fetch file", e.code)
            if response:
                logging.info("completed downloading file in : ", str((time.time() - startTime) * 1000) + "ms")
                fileName = file_url.split("/")[-1]
                with open(fileName, "wb") as f:
                    f.write(response.content)
                    f.close()
                while not os.path.exists(fileName):
                    time.sleep(1)

                if os.path.isfile(fileName):
                    pdfFileObject = open(fileName, 'rb')
                    startTime = time.time()
                    logger.info("extracting text from document")
                    text_to_return = str(extract_from_pdf(pdfFileObject, fileName), "UTF-8", "ignore")
                    logger.info(
                        "completed extracting text from file in : " + str((time.time() - startTime) * 1000) + "ms")
                    Path(fileName).rename(config.PROCESSED_FILE_PATH + fileName)
                    logger.info("save file, filepath:" + (config.PROCESSED_FILE_PATH + fileName))
                else:
                    raise CustomWebException("%s file does not exist" % fileName, 404)
        else:
            pdfFileObj = open(config.FILE_PATH + file_url, 'rb')
            text_to_return = str(extract_from_pdf(pdfFileObj, (config.FILE_PATH + file_url)), "utf-8", 'ignore')
            pdfFileObj.close()
    else:
        logging.exception("File format not supported" + file_url)
        raise CustomWebException("File format not supported", 400)

    return text_to_return


def sanitize_pdf(file):
    objects = []
    object_chunk = []
    for line in file.readlines():
        object_chunk.append(line)
        if object_chunk[-1] == b'endobj\n' and not b'/Type /Action\n' in object_chunk:
            objects = [*objects, *object_chunk]
            object_chunk = []
        elif object_chunk[-1] == b'%%EOF\n':
            objects = [*objects, *object_chunk]
            object_chunk = []
            break
        elif object_chunk[-1] == b'endobj\n':
            object_chunk = []

    return FileStorage([b''.join(objects), file.filename, file.filename, "application/pdf"])
