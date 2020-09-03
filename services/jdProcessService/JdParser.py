import time
import logging
import requests

from config import config
from utils.EXtractSkills import extract_skills

logger = logging.getLogger(__name__)


def parse_jd(jdParserRequest):
    startTime = time.time()
    logger.info('received request to parse jd')

    skillset = []

    if (jdParserRequest.skillFlag):
        # Extract skills
        skillset = extract_skills(jdParserRequest.jdString, bool(1))

    data = {"companyId": jdParserRequest.companyId, "selectedRole": {}, "industry": {},
            "function": {"functionName": jdParserRequest.function}, "skills": skillset}

    startTimeForSearchEngineCall = time.time()

    resp = requests.post(config.SEARCH_ENGINE_BASE_URL+config.SEARCH_ENGINE_GET_QUESTION_URL, json=data, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJyb2xlcyI6IisyUEw5S2hlaFRDakNOMDBYLy8yZHduOTNUazJsZG1ZeVZGNUJGS2FZNHM9IiwidXNlcklkIjoiT3gyanZpOWZJUUJHK3M1TFo2dlV0UT09IiwiY29tcGFueSI6IlVnUjIvL1dDZFYzRUhPRy9EVCtWTWc9PSIsInN1YiI6InFKazJsL2kzQnUxOUVxZnV3V3J0VlVzaW9Za0hUQ1Z3bXdRdjRTK0RvdDQ9IiwiaWF0IjoxNTk5MTE1MzE0LCJleHAiOjE1OTkyMDE3MTR9.8yjffkyoM2BOw531x4g-pfqO_5HpLcaTuVaNn75WxKATm-GZqTi44H5Kj6VWmvlaoJXK9P_FEV3gJJyaXLXojw'})

    logger.info('finished request to search engine to get question list per skill in : ' + str(
        (time.time() - startTimeForSearchEngineCall) * 1000) + ' ms')

    logger.info('finished request to parse jd in : ' + str((time.time() - startTime) * 1000) + ' ms')
    return resp
