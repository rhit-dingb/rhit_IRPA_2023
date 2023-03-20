
from enum import Enum
from typing import Dict, List
from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import json
import sys
import re
import aiohttp
import asyncio
from datetime import datetime, date, timedelta






sys.path.append('../')

from backendAPI.DataType import DataType
from fastapi import FastAPI, Request, HTTPException
from Parser.RasaCommunicator import RasaCommunicator
from DataManager.constants import DEFINITION
from DataManager.constants import CDS_DEFINITION_DATABASE_NAME
from Parser.JsonDataLoader import JsonDataLoader
from DataManager.constants import CDS_DATABASE_NAME_TEMPLATE
from DataManager.MongoDataManager import MongoDataManager
from Parser.MongoDBSparseMatrixDataWriter import MongoDBSparseMatrixDataWriter
from Parser.MongoDbNoChangeDataWriter import MongoDbNoChangeDataWriter

from Parser.ParserFacade import ParserFacade
from Parser.DataLoader import DataLoader
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from fastapi.middleware.cors import CORSMiddleware
from DataManager.constants import ANNUAL_DATA_REGEX_PATTERN, DEFINITION_DATA_REGEX_PATTERN
from UnansweredQuestions.UnansweredQuestionAnswerEngine import UnansweredQuestionAnswerEngine

from Parser.SparseMatrixDataParser import SparseMatrixDataParser
from Parser.NoChangeDataParser import NoChangeDataParser
from backendAPI.AuthenticationManager import AuthenticationManager
from UnansweredQuestions.MongoDBUnansweredQuestionConnector import MongoDBUnansweredQuestionConnector

from UnansweredQuestions.UnasweredQuestionDBConnector import UnansweredQuestionDbConnector
from CacheLayer.Cache import Cache
from CacheLayer.EventType import EventType
from CacheLayer.CacheEventPublisher import CacheEventPublisher
from CacheLayer.DataDeletionSubscriber import DataDeletionSubscriber
from CacheLayer.DataUploadSubscriber import DataUploadSubscriber
from CacheLayer.ModelChangeSubscriber import ModelChangeSubscriber
from CacheLayer.constants import SECTIONS_UPLOADED_KEY, START_YEAR_KEY, END_YEAR_KEY, DATA_DELETED_KEY
from backendAPI.constants import AUTHORIZATION_HEADER_KEY

from backendAPI.helper import getStartAndEndYearFromDataName
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
import os
from decouple import config

authenticationManager = AuthenticationManager()
mongoDbDataManager = MongoDataManager()
mongoDbDataManager = Cache(mongoDbDataManager)

rasaCommunicator = RasaCommunicator()
client = MongoClient(MONGO_DB_CONNECTION_STRING)
unansweredQuestionAnswerEngine = UnansweredQuestionAnswerEngine()
unansweredQuestionDbConnector : UnansweredQuestionDbConnector = MongoDBUnansweredQuestionConnector(unansweredQuestionAnswerEngine)
cacheEventPublisher = CacheEventPublisher()
dataDeletionSubscriber = DataDeletionSubscriber(EventType.DataDeletion, mongoDbDataManager)
dataUploadSubscriber = DataUploadSubscriber(EventType.DataUploaded, mongoDbDataManager)
modelChangeSubscriber = ModelChangeSubscriber(EventType.ModelChange, mongoDbDataManager)
cacheEventPublisher.subscribe(dataUploadSubscriber)
cacheEventPublisher.subscribe(dataDeletionSubscriber)
cacheEventPublisher.subscribe(modelChangeSubscriber)



asyncio.create_task(cacheEventPublisher.startObserver()) 
# loop.run_until_complete(test)


app = FastAPI()


#A list of allowed origins
origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://irpa-chatbot.csse.rose-hulman.edu:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 45
from fastapi import status


@app.get("/")
async def root():
    return {"message": "Hello, this is IRPA Common Dataset API Service"}


@app.get("/api/get_available_data/{dataType}")
async def getAllData(dataType : str):
    dataAvailable : List[str]= []
    if dataType == DataType.ANNUAL.value:
        pattern = re.compile(ANNUAL_DATA_REGEX_PATTERN, re.IGNORECASE)
        dataAvailable = mongoDbDataManager.getAllAvailableData(pattern)
    elif dataType == DataType.DEFINITION.value:
        pattern = re.compile(DEFINITION_DATA_REGEX_PATTERN, re.IGNORECASE)
        dataAvailable = mongoDbDataManager.getAllAvailableData(pattern)
        print("DATA FOUND")
        print(dataAvailable)

    return {"data": dataAvailable}

"""
Example Expected json body for cds data, for definitions, there is no yearFrom and yearTo
{
    "type": "annual"
    "dataName": "CDS_2020_2021"
    "data": {'General Info': 
    # [
    # {'Question': "What is Rose-Hulman's mailing address?", 'Answer': "Rose-Hulman's mailing address is 5500 Wabash Ave, Terre 
    # Haute, IN 47803", 'Complete Sentence?': 'Yes'}, 
    # {'Question': 'What is Rose-Hulman main phone number?', 'Answer': "Rose-Hulman's main phone number is (812) 877-1511", 'Complete Sentence?': 'Yes'}, 
    # {'Question': 'What is Rose-Hulman's www home page address / website?', 'Answer': "Rose-Hulman's website is www.rose-hulman.edu", 'Complete Sentence?': 'Yes'}, 
    # .....],
   #'Enrollment_General': [.....], 
#  }
}
"""
@app.post("/api/upload_data")
async def parse_data(request : Request):
    token = getToken(request)
    await verifyToken(token)

    jsonData = await request.json()
    # dataType = jsonData["type"]
    excelData = jsonData["data"]
  
    jsonCdsLoader = JsonDataLoader()
    outputName = ""
    if "dataName" in jsonData:
        outputName = jsonData["dataName"]
    if not outputName == "":
        try:
            jsonCdsLoader.loadData(excelData)
            # dataWriter = MongoDBSp arseMatrixDataWriter(outputName)
            # dataParser = SparseMatrixDataParser()c
            dataParser = NoChangeDataParser()
            dataWriter = MongoDbNoChangeDataWriter(outputName, client=client)
            parserFacade = ParserFacade(dataLoader=jsonCdsLoader, dataWriter=dataWriter, dataParser=dataParser)
            await parserFacade.parse()
 
            startYear, endYear = getStartAndEndYearFromDataName(outputName)
            # print(outputName)
            print(startYear, endYear)
            eventData = {SECTIONS_UPLOADED_KEY: [], START_YEAR_KEY: startYear, END_YEAR_KEY: endYear }
            sectionFullNames = jsonCdsLoader.getAllSectionDataFullName()
            for sectionFullName in sectionFullNames:
                splitted = sectionFullName.split("_")
                section = splitted[0]
                if not section in eventData[SECTIONS_UPLOADED_KEY]:
                    eventData[SECTIONS_UPLOADED_KEY].append(section)
        
            await cacheEventPublisher.notify(EventType.DataUploaded, eventData)
            return {"message": "Done", "uploadedAs": outputName}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong while parsing the input data")

    

@app.post("/api/get_section_and_subsection_for_data")
async def get_section_subsection_for_data(request : Request):
    jsonData = await request.json()
    print("JSON DATA")
    print(jsonData)
    dataName = jsonData["dataName"]
    sectionAndSubsections : Dict[str, List[str]] = mongoDbDataManager.getSectionAndSubsectionsForData(dataName)
    return {"data": sectionAndSubsections}


@app.post("/api/delete_data")
async def delete_data(request : Request):
    jsonData = await request.json()

    token : Annotated[str, Depends(oauth2_scheme)] = getToken(request)
    await verifyToken(token)

    try:
        toDelete = jsonData["dataName"]
        didDelete = mongoDbDataManager.deleteData(toDelete)
        if didDelete:
            eventData = {DATA_DELETED_KEY: toDelete}
            await cacheEventPublisher.notify(EventType.DataDeletion,eventData )
        print("DELETING DATA")
        return {"didDelete": didDelete}
    except Exception:
        raise HTTPException(status_code=500, detail="Deletion failed")


@app.get("/api/get_years_available")
async def get_years_available():
    yearsAvailable = mongoDbDataManager.getAllAvailableYearsSorted()
    print(yearsAvailable)
    response = {"data": yearsAvailable}
    return response

@app.post("/api/change_year")
async def change_selected_year(request : Request):
    print(request)
    jsonData = await request.json()
    conversationId = jsonData["conversationId"]
    startYear = jsonData["startYear"]
    endYear = jsonData["endYear"]
    entities ={"startYear": startYear, "endYear": endYear}
    try:
        async with aiohttp.ClientSession() as session:
            response = await rasaCommunicator.injectIntent("change_year", entities, session, conversationId )
            return {"message": "success"}
    except Exception:
        raise HTTPException(status_code=500, detail="change failed")

@app.get("/api/get_selected_year/{conversation_id}")
async def get_selected_year(conversation_id : str):
    async with aiohttp.ClientSession() as session:
        entities = {}
        response = await rasaCommunicator.injectIntent("get_year",entities , session, conversation_id )
        # print(response.keys())
        messages = response["messages"]
        print(messages)
        if len(messages) == 0:
              return {"selectedYear": None  }
        else:
            startYear = messages[0]
            endYear = messages[1]
            return {"selectedYear":[startYear, endYear] }


# General API for getting unanswered questions
@app.get("/questions")
async def get_unans_questions():
    unanswered_questions = unansweredQuestionDbConnector.getAllUnansweredQuestionAndAnswer()
    return unanswered_questions


@app.get("/answer_unanswered_question")
async def answer_unanswered_question(question: str):
    answers = unansweredQuestionAnswerEngine.answerQuestion(question)
    return {"answers": answers}

@app.put("/question_update")
async def handle_post_answer(request: Request):
    token = getToken(request)
    await verifyToken(token)
    jsonData = await request.json()
    answer = jsonData["answer"]
    questionId = jsonData["id"]
    unansweredQuestionDbConnector.provideAnswerToUnansweredQuestion(questionId, answer)


@app.delete("/question_delete")
async def handle_delete_answer(request: Request):
    token = getToken(request)
    await verifyToken(token)

    jsonData = await request.json()
    id = jsonData["id"]
    db = client.freq_question_db
    questions_collection = db.unans_question
    boo1 = questions_collection.delete_one({'_id': ObjectId(id)})
    if boo1:
        unansweredQuestionAnswerEngine.update()
        return {'message': 'question is successfull deleted'}
    else:
        return {'message': 'question maybe not found and issue occurred'}

@app.post("/question_add")
async def handle_add_unanswered_question(request : Request):
    jsonData = await request.json()
    question = jsonData["content"]
    chatbotAnswers = jsonData["chatbotAnswers"]
    return unansweredQuestionDbConnector.addNewUnansweredQuestion(question, chatbotAnswers)


#====================Below are the list of APIs for Freqency API==========================
CURRENT_INTENTIONS = ['enrollment', 'admission', 'high_school_units', 'basis_for_selection']
class UserFeedback(Enum):
    NO_FEEDBACK = "NO_FEEDBACK"
    HELPFUL = "HELPFUL"
    NOT_HELPFUL = "NOT_HELPFUL"

class QuestionCategory(Enum):
    ENROLLMENT = "ENROLLMENT"
    ADMISSION = "ADMISSION"
    HIGH_SCHOOL_UNITS = "HIGH_SCHOOL_UNITS"
    BASIS_FOR_SELECTION = "BASIS_FOR_SELECTION"
    
@app.put("/question_asked/")
async def handle_new_event(request: Request):
    jsonData = await request.json()
    content = jsonData["content"]
    intent = jsonData["intent"]
    feedback = jsonData["feedback"]
    timeAsked: datetime = datetime.now()
    db = client.freq_question_db
    freq_collection = db.cds_frequency
    content = str(content)
    if(len(list(freq_collection.find({"question_asked": content.lower()}))) == 0):
        boo1 = freq_collection.insert_one({
            "intent": intent,
            "user_feedback": feedback,
            "time_asked": timeAsked,
            "question_asked": content.lower()})
        if boo1:
            return {'message': 'data successfully inserted'}
        else:
            return {'message': 'errors occurred'}
    else:
        boo2 = freq_collection.update_one({'question_asked': content}, {'$set': {'user_feedback': feedback}})
        if boo2:
            return {'message': 'user feedback successfully updated'}
        else:
            return {'message': 'errors occurred while updating user stats'}

"""
Testing1:
PUT request: http://127.0.0.1:8000/question_asked/?intent=ADMISSION&feedback=NO_FEEDBACK&timeAsked=2023-01-01T12:00:00&content=What%20is%20rose%20rankings
---output: data successfully inserted; check Database for result
THEN!!!
--------
PUT request: http://127.0.0.1:8000/question_asked/?intent=ADMISSION&feedback=NOT_HELPFUL&timeAsked=2023-01-01T12:00:00&content=What%20is%20rose%20rankings
"""

@app.get("/general_stats/")
async def handle_new_event(endDate: datetime = datetime.now(), startDate_short: datetime = (datetime.now() - timedelta(days=30)), startDate_long: datetime = (datetime.now() - timedelta(days=365))):
    db = client.freq_question_db
    freq_collection = db.cds_frequency
    short_stats = list(freq_collection.find({"time_asked": {"$gte": startDate_short, "$lte": endDate}}))
    long_stats = list(freq_collection.find({"time_asked": {"$gte": startDate_long, "$lte": endDate}}))
    short_stats = json.loads(json_util.dumps(short_stats))
    long_stats = json.loads(json_util.dumps(long_stats))
    return short_stats

"""
Test 1: DEFAULT VIEW
GET request: http://127.0.0.1:8000/general_stats/
"""


""""
AUTHENTICATION API. Code reference from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# @app.post("/authenticate")
# async def login(request: Request):
#     jsonData = await request.json()
#     username = jsonData["username"]
  
#     loginSuccess = authenticationManager.checkIsAdmin(username)
#     return {"loggedIn": loginSuccess}


@app.post("/token")
async def authenticate(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    isAdmin = authenticationManager.checkIsAdmin(username)
    if not isAdmin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
   

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user

# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[str, Depends(get_current_user)]):
#     return current_user

# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}


#decrypt the token and verify the validity of the token, return the admin's username
async def verifyToken(token : Annotated[str, Depends(oauth2_scheme)]) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if token == None:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print("GOT USERNAME", username)
        if username is None:
            raise credentials_exception
        user = authenticationManager.checkIsAdmin(username)
        print("GOT USER", user)
        if user == None:
            raise credentials_exception
        
        return user
    except JWTError:

        raise credentials_exception


@app.get("/admins")
async def getAdmins(request : Request):
    token = getToken(request)
    verifyToken(token)
    adminList = authenticationManager.getAdmins()
    return adminList

# helper methods
def getToken(request : Request):
    if AUTHORIZATION_HEADER_KEY in request.headers:
        return request.headers[AUTHORIZATION_HEADER_KEY]
    else:
        return None
    