from Candidate import Candidate
from EXtractSkills import extract_skills
from ExtractEducation import extract_education
from ExtractEmail import extract_email
from ExtractMobile import extract_mobile_number
from ExtractName import extract_name
from services.FileService import convert_to_text


def extractData(parsed_text):
    candidate = Candidate()
    candidate.name = extract_name(parsed_text)
    if len(extract_mobile_number(parsed_text)) > 0:
        candidate.mobile = extract_mobile_number(parsed_text).split(",")[0] if "," in extract_mobile_number(
            parsed_text) else extract_mobile_number(parsed_text)
        candidate.altMobile = extract_mobile_number(parsed_text).split(",")[1] if "," in extract_mobile_number(
            parsed_text) else ""
    if len(extract_email(parsed_text)):
        candidate.email = extract_email(parsed_text)
    candidate.skills = extract_skills(parsed_text)
    candidate.education = extract_education(parsed_text)
    return candidate.toJSON()


def parseResume(fileName):
    text = convert_to_text(fileName)

    if text != "":
        return extractData(text)
