import textract
import config.config
from datetime import datetime, date
from Candidate import Candidate
from EXtractSkills import extract_skills
from ExtractEducation import extract_education
from ExtractEmail import extract_email
from ExtractMobile import extract_mobile_number
from ExtractPdf import extract_text_from_pdf
from services.FileService import convert_to_text


def extractData(parsed_text):
    # print(extract_name(parsed_text))
    candidate = Candidate()
    if len(extract_mobile_number(parsed_text))>0:
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
