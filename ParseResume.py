import logging
import time

from Models.Candidate import Candidate
from EXtractSkills import extract_skills
from ExtractEducation import extract_education
from ExtractEmail import extract_email
from ExtractMobile import extract_mobile_number
from ExtractName import extract_name
from services.FileService import convert_to_text

logger = logging.getLogger(__name__)


def extractData(parsed_text):
    candidate = Candidate()
    #extracting candidate name
    startTime = time.time()
    logger.info("extracting candidate name")
    candidate.candidateName = extract_name(parsed_text)
    candidate.firstName = candidate.candidateName.split( )[0]
    candidate.lastName=candidate.candidateName.split( )[len(candidate.candidateName.split( ))-1]
    logger.info("completed extracting candidate name in : "+str((time.time()-startTime)*1000)+"ms")

    #extracting candidate mobile numbers
    startTime = time.time()
    logger.info("extracting candidate mobiles")
    mobile_array = extract_mobile_number(parsed_text);
    if len(mobile_array) > 0:
        candidate.mobile = mobile_array[0]
        candidate.mobile = ''.join(candidate.mobile).replace(' ', '')
        candidate.mobile = candidate.mobile.replace('-','')
        if len(mobile_array) > 1 :
            candidate.alternateMobile = mobile_array[1]
            candidate.alternateMobile = ''.join(candidate.alternateMobile).replace(' ', '')
            candidate.alternateMobile = candidate.alternateMobile.replace('-', '')
    logger.info("completed extracting mobile numbers in : "+str((time.time()-startTime)*1000)+"ms")

    #extracting candidate email
    startTime = time.time()
    logger.info("extracting candidate email")
    if extract_email(parsed_text) is not None and len(extract_email(parsed_text))>0:
        candidate.email = extract_email(parsed_text)
    logger.info("completed extracting email in : "+str((time.time()-startTime)*1000)+"ms")

    #extracting candidate's skills
    startTime = time.time()
    logger.info("extracting candidate skills")
    candidate.candidateSkillDetails = extract_skills(parsed_text)
    logger.info("completed extrating candidate's skills in : "+str((time.time()-startTime)*1000)+"ms")

    #extracting candidate's education
    startTime = time.time()
    logger.info("extracting candidate education")
    candidate.candidateEducationDetails = extract_education(parsed_text)
    logger.info("completed extracting candidate's education in : "+str((time.time()-startTime)*1000)+"ms")

    #return Candidate object
    return candidate.toJSON()


def parseResume(fileName):
    startTime = time.time()
    logger.info('received request to parse resume: '+fileName)
    try:
        text = convert_to_text(fileName)
    except Exception as e:
        raise Exception(e)

    if text != "":
        Candidate = extractData(text)
        logger.info('finished parsing resume in : ' + str((time.time() - startTime)*1000) + ' ms')
        return Candidate;
