import textract

from datetime import datetime, date
from Candidate import Candidate
from EXtractSkills import extract_skills
from ExtractEducation import extract_education
from ExtractEmail import extract_email
from ExtractMobile import extract_mobile_number
from ExtractPdf import extract_text_from_pdf


def extractData(parsed_text):
    try:
        # print(extract_name(parsed_text))
        candidate = Candidate()
        candidate.mobile = extract_mobile_number(parsed_text).split(",")[0] if "," in extract_mobile_number(
            parsed_text) else extract_mobile_number(parsed_text)
        candidate.altMobile = extract_mobile_number(parsed_text).split(",")[1] if "," in extract_mobile_number(
            parsed_text) else ""
        candidate.email = extract_email(parsed_text)
        candidate.skills = extract_skills(parsed_text)
        candidate.education = extract_education(parsed_text)
        return candidate.toJSON()
    except:
        print("error while extracting data from parsed text")


def parseResume():
    text = ""
    # try:
    #    text = extract_text_from_pdf("/home/sameer/Desktop/rahul.pdf")
    # except:
    #    print("extract_text_from_pdf yielded nothing")

    try:
        text = textract.process("/home/sameer/Downloads/Sameer Reza Khan[1_0].doc").decode("UTF-8")
    except:
        print("text extract not yielded anything")

    if text != "":
        return extractData(text)
