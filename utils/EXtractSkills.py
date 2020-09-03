import ast
import logging
import time

import spacy
import requests

from config import config
logger = logging.getLogger(__name__)

# load pre-trained model
from spacy.lang.de.syntax_iterators import noun_chunks

from model.CandidateSkillDetails import CandidateSkillDetails

nlp = spacy.load('en_core_web_sm')


# noun_chunks = nlp.noun_chunks


def extract_skills(text_data, isJdText):
    nlp_text = nlp(text_data)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    startTimeForgetSkills = time.time()

    # call search engine api to get all skill set
    data = requests.get(config.SEARCH_ENGINE_BASE_URL + config.SEARCH_ENGINE_GET_SKILL_SET_URL,
                        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJyb2xlcyI6IisyUEw5S2hlaFRDakNOMDBYLy8yZHduOTNUazJsZG1ZeVZGNUJGS2FZNHM9IiwidXNlcklkIjoiT3gyanZpOWZJUUJHK3M1TFo2dlV0UT09IiwiY29tcGFueSI6IlVnUjIvL1dDZFYzRUhPRy9EVCtWTWc9PSIsInN1YiI6InFKazJsL2kzQnUxOUVxZnV3V3J0VlVzaW9Za0hUQ1Z3bXdRdjRTK0RvdDQ9IiwiaWF0IjoxNTk5MTE1MzE0LCJleHAiOjE1OTkyMDE3MTR9.8yjffkyoM2BOw531x4g-pfqO_5HpLcaTuVaNn75WxKATm-GZqTi44H5Kj6VWmvlaoJXK9P_FEV3gJJyaXLXojw'})

    logger.info('finished request to search engine to get mater data skills in : ' + str((time.time() - startTimeForgetSkills) * 1000) + ' ms')

    # extract skill list
    skills = ast.literal_eval(data.text)

    skillset = []

    # check for one-grams (example: python)
    for skillText in skills:
        if skillText.lower() in text_data.lower():
            if isJdText:
                skillset.append(skillText)
            else:
                candidateSkillDetails = CandidateSkillDetails()
                candidateSkillDetails.skill = skillText.lower().capitalize()
                skillset.append(candidateSkillDetails)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            if isJdText:
                skillset.append(skillText.lower())
            else:
                candidateSkillDetails = CandidateSkillDetails()
                candidateSkillDetails.skill = token.lower().capitalize()
                skillset.append(candidateSkillDetails)

    return skillset

