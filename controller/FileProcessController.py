import json
from collections import namedtuple

from flask import Flask, Response, Blueprint, request
import logging

from CustomException.CustomException import CustomWebException
from services.FileService import sanitize_pdf

app = Flask(__name__)

file_process_api = Blueprint('file_process_api', __name__)


@file_process_api.route("/sanitizeFile", methods=['POST'])
def sanitizeFile():
    # Check if file present in request
    if 'file' not in request.files:
        raise CustomWebException("No file present in request", 400,)

    file = request.files['file']
    # Call to service method
    response = Response(sanitize_pdf(file), mimetype="multipart/form-data")

    logging.info(response.data)
    return response
