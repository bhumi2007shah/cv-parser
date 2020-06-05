import pandas as pd
import spacy

# load pre-trained model
from spacy.lang.de.syntax_iterators import noun_chunks

from model.CandidateSkillDetails import CandidateSkillDetails

nlp = spacy.load('en_core_web_sm')


# noun_chunks = nlp.noun_chunks


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("../skills.csv", sep=",", usecols=['skills'], squeeze=True)

    # extract values
    skills = list(data.values)

    skillset = []

    # check for one-grams (example: python)
    for skillText in skills:
        if ' ' + skillText.lower() + ' ' in resume_text or ' ' + skillText.upper() + ' ' in resume_text:
            candidateSkillDetails = CandidateSkillDetails()
            candidateSkillDetails.skill = skillText.lower().capitalize()
            skillset.append(candidateSkillDetails)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            candidateSkillDetails = CandidateSkillDetails()
            candidateSkillDetails.skill = token.lower().capitalize()
            skillset.append(candidateSkillDetails)

    return skillset


def extract_skills(jd_text, isJdText):
    nlp_text = nlp(jd_text)

    # reading the csv file
    data = pd.read_csv("../skills.csv", sep=",", usecols=['skills'], squeeze=True)

    # extract values
    skills = list(data.values)

    skillset = []

    # check for one-grams (example: python)
    for skillText in skills:
        if ' ' + skillText.lower() + ' ' in jd_text or ' ' + skillText.upper() + ' ' in jd_text:
            skillset.append(skillText)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    return skillset
