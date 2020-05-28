import json

from neo4j import GraphDatabase
from neobolt.routing import READ_ACCESS
import logging
from config import config
import time
import requests

logger = logging.getLogger(__name__)

def print_neo4j_data():
    startTime = time.time()
    logger.info('received request to connect neo4j')
    responseObject = {};
    driver = GraphDatabase.driver(config.NEO4J_URL, auth=("neo4j", "hexagon"), encrypted=False)
    session = driver.session(default_access_mode=READ_ACCESS)
    result = session.run("MATCH (c:Company) where c.companyName = 'Whiz.AI' return c")
    logger.info('finished connection to neo4j in : ' + str((time.time() - startTime) * 1000) + ' ms')
    for record in result.graph().nodes:
        for key, value in record.items():
            responseObject[key] = value
    return json.dumps(responseObject);

def get_neo4j_data_by_api():
    startTime = time.time()
    logger.info('received request to get neo4j data by api call')
    resp = requests.post(config.SEARCH_ENGINE_URL, json={"companyId": 111,"selectedRole": {"roleName": "VOLTE Engineer"},"industry": {"industryName": "IT"},"function": { },"skills":[]},
                         headers={'Content-Type': 'application/json'})
    logger.info('finished get neo4j data by api call in : ' + str((time.time() - startTime) * 1000) + ' ms')
    return resp

