import io
from pathlib import Path

import requests
import os.path
import time
import logging

from flask import jsonify

from ExtractDoc import extract_text_from_doc
from ExtractPdf import extract_from_pdf
from config import config
from Exception import WebException

logger = logging.getLogger(__name__)


def convert_to_text(file_url):
    text_to_return=""
    if "doc" in file_url or "docx" in file_url:
        if "http" in file_url or "https" in file_url:
            startTime = time.time()
            logger.info("downloading file: "+file_url)
            try:
                response = requests.get(file_url, stream=True)
            except Exception as e:
                logging.exception(e)
                raise Exception("Failed to fetch file", e.code)
            if response:
                logging.info("completed downloading file in : ", str((time.time()-startTime)*1000)+"ms")
                fileName = file_url.split("/")[-1]
                with open(fileName, "wb") as f:
                    f.write(response.content)
                    f.close()
                startTime = time.time()
                logger.info("extracting text from document")
                text_to_return = extract_text_from_doc(fileName)
                logger.info("completed extracting text from file in : "+str((time.time()-startTime)*1000)+"ms")
                Path(fileName).rename(config.PROCESSED_FILE_PATH+fileName)
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
                raise Exception("Failed to fetch file", e.code)
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
                    logger.info("completed extracting text from file in : " + str((time.time() - startTime) * 1000)+"ms")
                    Path(fileName).rename(config.PROCESSED_FILE_PATH+fileName)
                    logger.info("save file, filepath:"+(config.PROCESSED_FILE_PATH+fileName))
                else:
                    raise ValueError("%s file does not exist" % fileName)
        else:
            pdfFileObj = open(config.FILE_PATH+file_url, 'rb')
            text_to_return = str(extract_from_pdf(pdfFileObj, (config.FILE_PATH+file_url)), "utf-8", 'ignore')
            pdfFileObj.close()

    return text_to_return
