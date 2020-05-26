from neo4j import GraphDatabase
from neobolt.routing import READ_ACCESS
import logging
import time

logger = logging.getLogger(__name__)

uri = "bolt://localhost:7687"

def print_neo4j_data():
    startTime = time.time()
    logger.info('received request to connect neo4j')
    driver = GraphDatabase.driver(uri, auth=("neo4j", "hexagon"), encrypted=False)
    session = driver.session(default_access_mode=READ_ACCESS)
    result = session.run("MATCH (n:Company) where n.companyName = 'MindTree' return n;")
    logger.info('finished connection to neo4j in : ' + str((time.time() - startTime) * 1000) + ' ms')
    return [record["n"] for record in result]
