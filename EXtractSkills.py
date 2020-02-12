import pandas as pd
import spacy

# load pre-trained model

nlp = spacy.load('en_core_web_sm')
# noun_chunks = nlp.noun_chunks


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("skills.csv", sep=",", usecols=['skills'], squeeze=True)

    # extract values
    skills = list(data.values)

    skillset = []

    # check for one-grams (example: python)
    for skill in skills:
        if ' '+skill.lower()+' ' in resume_text:
            skillset.append(skill)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            candidateSkillDetails = {}
            candidateSkillDetails["skill"] = token
            skillset.append(candidateSkillDetails)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]