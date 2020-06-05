import json
from collections import namedtuple

from flask import Flask, Response, Blueprint, request
import logging

from objectmapper import ObjectMapper

from services.JdParserRequest import JdParserRequest
from services.jdProcessService.JdParser import get_neo4j_data_by_api, parse_jd

app = Flask(__name__)

jd_process_api = Blueprint('jd_process_api', __name__)


@jd_process_api.route("/getNeo4jData", methods=['GET'])
def callNeo4jApi():
    response = Response(get_neo4j_data_by_api(), mimetype="application/json")
    logging.info(response)
    logging.info(response.data)
    return response


class SearchEngineRequest(object):
    pass


@jd_process_api.route("/parseJd", methods=['POST'])
def parseJd():

    # Parse JSON into an object with attributes corresponding to dict keys.
    jdParserRequest = json.loads(request.data.decode('utf8').replace("'", '"'), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    # Call to service method
    response = Response(parse_jd(jdParserRequest), mimetype="application/json")

    logging.info(response.data)
    return response
