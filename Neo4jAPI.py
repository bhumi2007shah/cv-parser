from flask import Flask, Response, Blueprint
import logging

from Neo4jConnect import print_neo4j_data, get_neo4j_data_by_api

app = Flask(__name__)

neo4j_api = Blueprint('neo4j_api', __name__)


@neo4j_api.route("/neo4j", methods=['GET'])
def neo4jDbConnect():
    response = Response(print_neo4j_data(), mimetype="application/json")
    logging.info(response)
    logging.info(response.data)
    return response


@neo4j_api.route("/getNeo4jData", methods=['GET'])
def callNeo4jApi():
    response = Response(get_neo4j_data_by_api(), mimetype="application/json")
    logging.info(response)
    logging.info(response.data)
    return response
