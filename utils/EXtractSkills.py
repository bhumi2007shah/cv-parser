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
                        headers={'Content-Type': 'application/json'})

    logger.info('finished request to search engine to get mater data skills in : ' + str((time.time() - startTimeForgetSkills) * 1000) + ' ms')

    # extract skill list
    skills = ast.literal_eval(data.text)

    skillset = []

    # check for one-grams (example: python)
    for skillText in skills:
        if ' ' + skillText.lower() + ' ' in text_data or ' ' + skillText.upper() + ' ' in text_data:
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
                skillset.append(skillText)
            else:
                candidateSkillDetails = CandidateSkillDetails()
                candidateSkillDetails.skill = token.lower().capitalize()
                skillset.append(candidateSkillDetails)

    return skillset

