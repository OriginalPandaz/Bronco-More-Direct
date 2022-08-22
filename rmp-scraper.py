#documentationOnAPI: https://pypi.org/project/RateMyProfessorAPI/
#python -m pip install RateMyProfessorAPI
#Runs on Python 3.9.0 > : Tested on 3.10.0

from tokenize import String
from typing import Dict
import ratemyprofessor

#name = "Frank Mathur"
#site = "Pomona"

Dict = {}

def fetch_professor_data(name, site, expdate):
    professor = ratemyprofessor.get_professor_by_school_and_name(
    ratemyprofessor.get_school_by_name(site), name)
    if professor is not None:
        takeAgain = ""
        name = (professor.name).split()
        firstName = name[0]
        lastName = name[1]

    if professor is not None:
        takeAgain = ""

    if professor.would_take_again is not None:
        takeAgain = round(professor.would_take_again, 1)
    else:
        takeAgain =  "N/A"

    Dict = {
        'professorFirst' : firstName,
        'professorLast' : lastName,
        'schoolName' : professor.school.name,
        'department' : professor.department,
        'id' : professor.id,
        'professorRating' : professor.rating,
        'difficulty' : professor.difficulty,
        'takeAgainPercent' : takeAgain,
        'expdate' : expdate
    }

    return Dict

def lambda_handler(event, context):
    classes = fetch_professor_data(event['name'],event['site'],event['expdate'])
    return classes
