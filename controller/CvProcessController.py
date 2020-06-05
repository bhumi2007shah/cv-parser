import logging
from flask import Flask, Response, request, Blueprint
from services.FileService import convert_to_text
from services.cvProcessService.ParseResume import parseResume

app = Flask(__name__)

cv_process_api = Blueprint('cv_process_api', __name__)


@cv_process_api.route("/parsecv", methods=['GET'])
def parsecv():
    fileName = request.args.get("file")
    response = Response(parseResume(fileName), mimetype="application/json")
    logging.info(response)
    logging.info(response.data)
    return response


@cv_process_api.route("/textconvert", methods=['GET'])
def textconvert():
    fileName = request.args.get("file")
    logging.info("Received request to extract text for file : " + fileName)
    response = Response(convert_to_text(fileName), mimetype="text/plain")
    logging.info(response)
    logging.info(response.data)
    return response
