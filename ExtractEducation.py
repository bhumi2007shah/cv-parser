import re
import spacy
from nltk.corpus import stopwords

# load pre-trained model
from Models.CandidateEducationDetails import CandidateEducationDetails

nlp = spacy.load('en_core_web_sm')

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'Bachelor of Engineering',
    'ME', 'M.E', 'M.E.', 'MS', 'M.S',
    'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
    'SSC', 'HSC', 'X', 'XII', '10TH', '12TH'
]


def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                try:
                    edu[tex] = text + nlp_text[index + 1]
                except Exception as e:
                    print(str(e))

    # Extract Branch
    # Extract year
    education = []
    for key in edu.keys():
        year = re.findall(re.compile(r'(?:(?:20|19)(?:\d{2}))+'), edu[key])
        educationObject = CandidateEducationDetails()
        if year:
            educationObject.degree = key
            if len(year) > 1:
                educationObject.yearOfPassing = ''.join(year[1])
            else:
                educationObject.yearOfPassing = ''.join(year[0])
        else:
            educationObject.degree = key

        education.append(educationObject.toJSON())
    return education
