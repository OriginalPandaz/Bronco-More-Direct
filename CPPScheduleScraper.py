from requests.api import head
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
import re
from enum import Enum, auto
import time

class ClassSubject(Enum):
    ABM = auto(),
    ACC = auto(),
    AG = auto(),
    AGS = auto(),
    AH = auto(),
    AHS = auto(),
    AMM = auto(),
    ANT = auto(),
    ARC = auto(),
    ARO = auto(),
    AST = auto(),
    AVS = auto(),
    BIO = auto(),
    BUS = auto(),
    CE = auto(),
    CHE = auto(),
    CHM = auto(),
    CHN = auto(),
    CIS = auto(),
    CLS = auto(),
    CM = auto(),
    COM = auto(),
    CPU = auto(),
    CRM = auto(),
    CS = auto(),
    DAN = auto(),
    EBZ = auto(),
    EC = auto(),
    ECE = auto(),
    ECI = auto(),
    ECS = auto(),
    EDD = auto(),
    EDL = auto(),
    EDU = auto(),
    EGR = auto(),
    EMT = auto(),
    ENG = auto(),
    ENV = auto(),
    ERA = auto(),
    ETE = auto(),
    ETM = auto(),
    EWS = auto(),
    FRE = auto(),
    FRL = auto(),
    FST = auto(),
    GBA = auto(),
    GEO = auto(),
    GER = auto(),
    GSC = auto(),
    HRT = auto(),
    HST = auto(),
    IAM = auto(),
    IBM = auto(),
    IE = auto(),
    IGE = auto(),
    IME = auto(),
    INA = auto(),
    IPC = auto(),
    KIN = auto(),
    LA = auto(),
    LIB = auto(),
    LRC = auto(),
    LS = auto(),
    MAT = auto(),
    ME = auto(),
    MFE = auto(),
    MHR = auto(),
    MPA = auto(),
    MSL = auto(),
    MTE = auto(),
    MU = auto(),
    TR = auto(),
    PHL = auto(),
    PHY = auto(),
    PLS = auto(),
    PLT = auto(),
    PSY = auto(),
    RS = auto(),
    SCI = auto(),
    SE = auto(),
    SME = auto(),
    SOC = auto(),
    SPN = auto(),
    STA = auto(),
    STS = auto(),
    SW = auto(),
    TH = auto(),
    TOM = auto(),
    URP = auto(),
    VCD = auto()

class CourseComponent(Enum):
    ACTIVITY = "ACT"
    CLINICAL = "CLN"
    INDEPENDENT_STUDY = "IND"
    LABORATORY = "LAB"
    LECTURE = "LEC"
    PRACTICUM = "PRA"
    SEMINAR = "SEM"
    SUPERVISION = "SUP"
    THESIS_RESEARCH = "THE"

class CourseAttribute(Enum):
    ANY = "Any Attribute"                                      #Any Attribute
    AMP = "ACP|NULL"                                           #American Cultural Perspectives
    A = "GE-A|NULL"                                            #Area A-Eng Lang Com Crtcl Thnk
    A1 = "GE-A|A-1"                                            #A-1 Oral Communication
    A2 = "GE-A|A-2"                                            #A-2 Written Communication
    A3 = "GE-A|A-3"                                            #A-3 Critical Thinking
    B = "GE-B|NULL"                                            #Area B-Sci Inquiry &amp; Quant Rsn
    B1 = "GE-B|B-1"                                            #B-1 Physical Sciences
    B2 = "GE-B|B-2"                                            #B-2 Life Sciences
    B3 = "GE-B|B-3"                                            #B-3 Laboratory Activity
    B4 = "GE-B|B-4"                                            #B-4 Math/Quant Reasoning
    B5 = "GE-B|B-5"                                            #B-5 Science and Tech Synthesis
    C = "GE-C|NULL"                                            #Area C-Arts and Humanities
    C1 = "GE-C|C-1"                                            #C-1 Visual &amp; Performing Arts
    C2 = "GE-C|C-2"                                            #C-2 Lit, Mod Lng, Phl &amp; Cvlztn
    C3 = "GE-C|C-3"                                            #C-3 Arts &amp; Humanities Synth
    D = "GE-D|NULL"                                            #Area D-Social Sciences
    D1 = "GE-D|D-1"                                            #D-1 US History American Ideals
    D2 = "GE-D|D-2"                                            #D-2 US Constitution &amp; CA Gvmnt
    D3 = "GE-D|D-3"                                            #D-3 SocSci:Prn, Mthd, Val, Eth
    D4 = "GE-D|D-4"                                            #D-4 Social Science Synthesis
    E = "GE-E|NULL"                                            #Area E-Lifelong Undst/Self Dev
    F = "GE-F|NULL"                                            #Area F-Ethnic Studies
    GRADUATE_DIVISION = "CLEV|3"                               #Course Level: Graduate Division
    LOWER_DIVISION = "CLEV|1"                                  #Course Level: Lower Division
    UPPER_DIVISION = "CLEV|2"                                  #Course Level: Upper Division
    ACTIVITY = "CSFX|A"                                        #Activity
    HONORS = "CSFX|H"                                          #Honors
    LABORATORY = "CSFX|L"                                      #Laboratory
    SERVICE_LEARNING = "CSFX|S"                                #Service Learning
    HONORS_ACTIVITY = "CSFX|AH"                                #Honors Activity
    HONORS_SERVICE_LEARNING_ACTIVITY = "CSFX|AHS"              #Honors Service Learning Act
    SERVICE_LEARNING_ACTIVITY = "CSFX|AS"                      #Service Learning Activity
    HONORS_SERVICE_LEARNING = "CSFX|HS"                        #Honors Service Learning
    HONORS_LABORATORY = "CSFX|LH"                              #Honors Laboratory
    HONORS_SERVICE_LEARNING_LABORATORY = "CSFX|LHS"            #Honors Service Learning Laboratory
    SERVICE_LEARNING_LABORATORY = "CSFX|LS"                    #Service Learning Laboratory
    MULTILINGUAL = "CSFX|M"                                    #Multilingual
    EXTRA_CREDIT_COMMUNITY_ENGLISH_LEARNING = "CCEL|EC"        #Extra Credit Cmty Eng Lrng
    OPTIONAL_COMMUNITY_ENGLISH_LEARNING = "CCEL|O"             #Optional Cmty Eng Lrng
    REQUIRED_COMMUNITY_ENGLISH_LEARNING = "CCEL|R"             #Required Cmty Eng Lrng
    EXTRA_CREDIT_SERVICE_LEARNING = "CSLI|EC"                  #Extra Credit Service Learning
    OPTIONAL_SERVICE_LEARNING_COURSE = "CSLI|O"                #Optional Service Learning Crse
    REQUIRED_SERVICE_LEARNING_COURSE = "CSLI|R"                #Required Service Learning Crse
    EXTENDED_EDUCATION = "CCTP|2"                              #Extended Education
    UNIVERSITY_OPEN_UNIVERSITY = "CCTP|1"                      #University Open University
    ZERO_COST_COURSE_MATERIALS = "ZCCM|ZCCM"                   #Zero Cost Course Materials
    ONLINE = "FONL|AB386"                                      #Online
    COURSE_MATCH = "FONL|CM"                                    #Course Match

class CourseCareer(Enum):
    ANY = "Any Career"
    NON_CREDIT_EXTENSION = "EXED"
    GRADUATE = "GRAD"
    GRADUATE_POSTBACCALAUREATE = "PBAC"
    UNDERGRADUATE = "UGRD"

class InstructionMode(Enum):
    ANY_MODE = "Any Mode"
    ASYNCHRONOUS_LOCAL = "AL"
    FACE_TO_FACE = "P"
    FULLY_ASYNCHRONOUS = "A"
    FULLY_SYNCHRONOUS = "S"
    HYBRID = "H"
    HYBRID_ASYNCHRONOUS_COMPONENT = "HA"
    HYBRID_SYNCHRONOUS_COMPONENT = "HS"
    SYNCHRONOUS_LOCAL = "SL"
    WEB_ASSISTED = "PW"
    UNKNOWN = "B"

class CourseSession(Enum):
    ANY_SESSION = "Any Session"
    FIRST_3_WEEK_SESSION = "OUT"
    FIRST_TWO_WEEK_SESSION = "OUA"
    SECOND_3_WEEK_SESSION = "OUU"
    SECOND_TWO_WEEK_SESSION = "OUB"
    THIRD_TWO_WEEK_SESSION = "OUC"
    FOURTH_TWO_WEEK_SESSION = "OUD"
    ESP_10_WEEK_SESSION = "OUE"
    ESP_1ST_5_WEEK_SESSION = "OUF"
    ESP_2ND_5_WEEK_SESSION = "OUG"
    ESP_6_WEEK_SESSION = "OUI"
    ESP_8_WEEK_SESSION = "OUH"
    EXTENSION_SESSION = "EXT"
    EXTENSION_SESSION_1ST_5WK = "EX1"
    FIVE_WEEK_FIRST = "5W1"
    FIVE_WEEK_SECOND = "5W2"
    OPEN_UNIVERSITY_1ST_5WK = "OU1"
    OPEN_UNIVERSITY_2ND_5WK = "OU2"
    OPEN_UNIVERSITY_QUARTER_SB = "OUQ"
    PEN_UNIVERSITY_SESSION = "OU"
    OPEN_UNIVERSITY_SUM09 = "OUS"
    RGULAR_ACADEMIC_SESSION = "1"
    SIX_WEEK_SECOND = "6W2"
    SPECIAL_SESSION_FIRST_5_WEEKS = "SP1"
    SPECIAL_SESSION_SECOND_5_WEEKS = "SP2"
    SPECIAL_SESSION_DEGREE = "SPD"
    SPECIAL_SESSION_QUARTER = "QTR"
    SPECIAL_SESSION_QUARTER_WINTER = "QTW"
    UNKNOWN = "OUS"

class CourseTime(Enum):
    ONE_AM = "01:00:00 AM"
    TWO_AM = "02:00:00 AM"
    THREE_AM = "03:00:00 AM"
    FOUR_AM = "04:00:00 AM"
    FIVE_AM = "05:00:00 AM"
    SIX_AM = "06:00:00 AM"
    SEVEN_AM = "07:00:00 AM"
    EIGHT_AM = "08:00:00 AM"
    NINE_AM = "09:00:00 AM"
    TEN_AM = "10:00:00 AM"
    ELEVEN_AM = "11:00:00 AM"
    TWELVE_PM = "12:00:00 PM"
    ONE_PM = "01:00:00 PM"
    TWO_PM = "02:00:00 PM"
    THREE_PM = "03:00:00 PM"
    FOUR_PM = "04:00:00 PM"
    FIVE_PM = "05:00:00 PM"
    SIX_PM = "06:00:00 PM"
    SEVEN_PM = "07:00:00 PM"
    EIGHT_PM = "08:00:00 PM"
    NINE_PM = "09:00:00 PM"
    TEN_PM = "10:00:00 PM"
    ELEVEN_PM = "11:00:00 PM"
    TWELVE_AM = "12:00:00 AM"

class ClassDays(Enum):
    MONDAY = "0"
    TUESDAY = "1"
    WEDNESDAY = "2"
    THURSDAY = "3"
    FRIDAY = "4"
    SATURDAY = "5"
    SUNDAY = "6"
    TBA = "7"

def buildSearchParams(
    term = None,
    subject = None,
    catalogNumber = None,
    subjectExactMatch = None,
    title = None,
    courseComponent = None,
    courseAttribute = None,
    courseCareer = None,
    instructionMode = None,
    courseSession = None,
    possibleDays = None,
    startTime = None,
    endTime = None,
    instructor = None):
    params = {}
    params["ctl00$ContentPlaceHolder1$TermDDL"] = term if term is not None else '2217'
    params["ctl00$ContentPlaceHolder1$ClassSubject"] = subject.name
    params["ctl00$ContentPlaceHolder1$CatalogNumber"] = catalogNumber
    if subjectExactMatch == True:
        params["ctl00$ContentPlaceHolder1$CourseComponentDDL"] = courseComponent.value if courseComponent is not None else 'Any Component'
    params["ctl00$ContentPlaceHolder1$CourseAttributeDDL"] = courseAttribute.value if courseAttribute is not None else 'Any Attribute'
    params["ctl00$ContentPlaceHolder1$CourseCareerDDL"] = courseCareer.value if courseCareer is not None else 'Any Career'
    params["ctl00$ContentPlaceHolder1$InstModesDDL"] = instructionMode.value if instructionMode is not None else 'Any Mode'
    params["ctl00$ContentPlaceHolder1$SessionDDL"] = courseSession.value if courseSession is not None else 'Any Session'
    if possibleDays == None:
        for i in range(8):
            params["ctl00$ContentPlaceHolder1$ClassDays$" + str(i)] = "on"
    else:
        for day in possibleDays:
            params["ctl00$ContentPlaceHolder1$ClassDays$" + str(day.value)] = "on"
    params["ctl00$ContentPlaceHolder1$StartTime"] = startTime.value if startTime is not None else 'ANY'
    params["ctl00$ContentPlaceHolder1$EndTime"] = endTime.value if endTime is not None else 'ANY'
    params["ctl00$ContentPlaceHolder1$Instructor"] = instructor if instructor is not None else ''
    params["ctl00$ContentPlaceHolder1$SearchButton"] = "Search"

    return params

def convertTerm(term):
    value = 2187
    if term == None: return str(value)
    if term[0:2].lower() == "fa":
        value += 10 * (int(term[2:4]) - 18)
    elif term[0:2].lower() == "sp":
        value += 10 * (int(term[2:4]) - 18) - 4
    elif term[0:2].lower() == "su":
        value += 10 * (int(term[2:4]) - 18) - 6

    return str(value)

def fetch_class_data(term, subject, number):
    url = 'https://schedule.cpp.edu'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    params = buildSearchParams(term=convertTerm(term), subject=ClassSubject[subject.upper()], catalogNumber=number)
    data = {}
    sectionList = []
    session = requests.Session()

    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    secrets = soup.select("#aspnetForm > div > input")

    for x in secrets:
        data[x['id']] = x['value']

    for x in params:
        if params[x] != None:
            data[x] = params[x]

    #print(data)

    response = session.post(url, headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')

    class_list = soup.find('div', id='class_list')

    titleIndex = 1
    for data in class_list.find_all('li'):
        parsedTitle = data.find('td', id='ctl00_ContentPlaceHolder1_Repeater1_ctl0' + str(titleIndex) + '_TableCell8').text
        time_days = data.find('td', id ='ctl00_ContentPlaceHolder1_Repeater1_ctl0' + str(titleIndex) + '_TableCell1').text
        building = data.find('td', id='ctl00_ContentPlaceHolder1_Repeater1_ctl0' + str(titleIndex) + '_TableCell2').text
        semesterLen = data.find('td', id='ctl00_ContentPlaceHolder1_Repeater1_ctl0' + str(titleIndex) + '_TableCell12').text
        sessionType = data.find('td', id='ctl00_ContentPlaceHolder1_Repeater1_ctl0' + str(titleIndex) + '_TableCell17').text
        sectionList.append(extractSectionData(data.text.strip(), parsedTitle, time_days, building, semesterLen, sessionType))
        titleIndex += 1

    return sectionList

def extractSectionData(text, parsedTitle, time_days, building, semesterLen, sessionType):
    splitText = text.split()
    return SectionDataDto(
        subject = splitText[0],
        catalogNumber = splitText[1],
        sectionNumber = splitText[3],
        classNumber = splitText[5][3:8],
        capacity = splitText[5][16:len(splitText[5])],
        title = parsedTitle,
        units = splitText[5 + len(parsedTitle.split())][len(splitText[5 + len(parsedTitle.split())])-1],
        time = " ".join(re.split('\s+', time_days, flags=re.UNICODE)).replace('–','-'),
        location = building,
        date = " ".join(re.split('\s+', semesterLen, flags = re.UNICODE)),
        session = sessionType,
        instructorLast = splitText[len(splitText)-4][:-1],
        instructorFirst = splitText[len(splitText)-3],
        mode = splitText[len(splitText)-1],
        component = splitText[len(splitText)-2][12:-1]
    )

sections =  fetch_class_data('sp22', 'cs', '2400')

def lambda_handler(event, context):
    classes = fetch_class_data(event['term'], event['subject'], event['number'])
    return classes
