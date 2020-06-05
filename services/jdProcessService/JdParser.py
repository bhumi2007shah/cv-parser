import time
import logging
import requests

from config import config
from utils.EXtractSkills import extract_skills

logger = logging.getLogger(__name__)


def get_neo4j_data_by_api():
    startTime = time.time()
    logger.info('received request to get neo4j data by api call')
    resp = requests.post(config.SEARCH_ENGINE_URL,
                         json={"companyId": 111, "selectedRole": {"roleName": "VOLTE Engineer"},
                               "industry": {"industryName": "IT"}, "function": {}, "skills": []},
                         headers={'Content-Type': 'application/json'})
    logger.info('finished get neo4j data by api call in : ' + str((time.time() - startTime) * 1000) + ' ms')
    return resp


def parse_jd(jdParserRequest):
    startTime = time.time()
    logger.info('received request to parse jd')

    skillset = []

    if (jdParserRequest.skillFlag):
        # Extract skills
        skillset = extract_skills(jdParserRequest.jdString, jdParserRequest.skillFlag)

    data = {"companyId": jdParserRequest.companyId, "selectedRole": {}, "industry": {}, "function": {"functionName": jdParserRequest.function},"skills": skillset}

    startTimeForSearchEngineCall = time.time()

    resp = requests.post(config.SEARCH_ENGINE_URL, json=data, headers={'Content-Type': 'application/json'})

    logger.info('finished request to search engine to get question list per skill in : ' + str((time.time() - startTimeForSearchEngineCall) * 1000) + ' ms')

    logger.info('finished request to parse jd in : ' + str((time.time() - startTime) * 1000) + ' ms')
    return resp
