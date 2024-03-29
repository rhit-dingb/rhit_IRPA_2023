
from enum import Enum
from typing import Dict, List, Union
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
from Parser.MongoDbNoChangeDataWriter import MongoDbNoChangeDataWriter

from Parser.ParserFacade import ParserFacade
from Parser.DataLoader import DataLoader
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from fastapi.middleware.cors import CORSMiddleware
from DataManager.constants import ANNUAL_DATA_REGEX_PATTERN, DEFINITION_DATA_REGEX_PATTERN
from UnansweredQuestions.UnansweredQuestionAnswerEngine import UnansweredQuestionAnswerEngine
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
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.ConvertToSparseMatrixDecorator import ConvertToSparseMatrixDecorator

from backendAPI.constants import EVENT_OCCURED_KEY
import nltk

try:
    nltk.find('corpora/wordnet')
except Exception:
    nltk.download('wordnet')

try:
    nltk.find('omw-1.4')
except Exception:
    nltk.download('omw-1.4')



authenticationManager = AuthenticationManager()

mongoProcessor = MongoProcessor()
mongoProcessor = ConvertToSparseMatrixDecorator(mongoProcessor)
mongoDbDataManager = MongoDataManager(mongoProcessor=mongoProcessor)
mongoDbDataManager = Cache(mongoDbDataManager)

rasaCommunicator = RasaCommunicator()
client = MongoClient(MONGO_DB_CONNECTION_STRING)

unansweredQuestionDb =client.freq_question_db
unansweredQuestionDbConnector : UnansweredQuestionDbConnector = MongoDBUnansweredQuestionConnector(unansweredQuestionDb)
unansweredQuestionAnswerEngine = UnansweredQuestionAnswerEngine(unansweredQuestionDbConnector)

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
ACCESS_TOKEN_EXPIRE_MINUTES = 240
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
            # dataParser = SparseMatrixDataParser()
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


            entities ={"eventType":"dataUploaded", "dataName":outputName}
            if startYear and endYear:
                entities["startYear"] = startYear
                entities["endYear"]  = endYear

            async with aiohttp.ClientSession() as session:
                response = await rasaCommunicator.injectIntent(EVENT_OCCURED_KEY, entities, session, "random")
                print(response)
    
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
        
        entities ={"eventType":"dataDeleted", "dataName": toDelete}
        async with aiohttp.ClientSession() as session:
            response = await rasaCommunicator.injectIntent(EVENT_OCCURED_KEY, entities, session, "random")
            

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


# ==================================API for getting unanswered questions===============================================
@app.get("/questions")
async def get_unans_questions():
    unanswered_questions = unansweredQuestionDbConnector.getAllUnansweredQuestionAndAnswer()
    return unanswered_questions

@app.get("/questions/{question_id}")
async def get_question_by_id(question_id : str):
    questionObj = unansweredQuestionDbConnector.getQuestionAnswerObjectById(question_id)
    return questionObj

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
    unansweredQuestionAnswerEngine.questionAnswered(questionId)


@app.delete("/question_delete")
async def handle_delete_answer(request: Request):
    token = getToken(request)
    await verifyToken(token)

    jsonData = await request.json()
    id = jsonData["id"]
    # db = client.freq_question_db
    # questions_collection = db.unans_question
    # boo1 = questions_collection.delete_one({'_id': ObjectId(id)})
    deleteSuccess = unansweredQuestionDbConnector.deleteUnansweredQuestion(id)
    if deleteSuccess:
        unansweredQuestionAnswerEngine.questionDeleted(id)
        return {'message': 'question is successfull deleted'}
    else:
        return {'message': 'question maybe not found and issue occurred'}



@app.post("/question_add")
async def handle_add_unanswered_question(request : Request):
    jsonData = await request.json()
    question = jsonData["content"]
    chatbotAnswers : List[Dict[str, any]] = jsonData["chatbotAnswers"]
    # print(chatbotAnswers)
    success = unansweredQuestionDbConnector.addNewUnansweredQuestion(question, chatbotAnswers)
    if success:
        print("QUESTION ADDED SUCCESSFULLY")
        return {'message': 'question is successfull added'}
    else:
        print("ERROR OCCURED DURING QUESTION ADD")
        return {'message': 'errors occurred during question add'}


# This can either be administrator or user, so we need to the isAdministrator field to determine
@app.put("/update_answer_feedback")
async def update_answer_feedback(request : Request):
    request = await request.json()
    isAdministrator = request["isAdmin"]
    feedback = request["feedback"]
    chatbotAnswer = request["chatbotAnswer"]
    
    # if not isAdministrator:
    #     # otherwise it is user and if they put down vote button, then save to database.
    #     if feedback == "incorrect":

    # else:
    questionId = request["questionId"]
    result = unansweredQuestionDbConnector.updateFeedbackForAnswer(questionId=questionId, chatbotAnswer=chatbotAnswer, feedback=feedback)
    return {"success": result}




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
        else:\
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
async def handle_new_event(endDate: datetime = datetime.now(), startDate_short: datetime = None, startDate_long: datetime = None):
    db = client.freq_question_db
    freq_collection = db.cds_frequency
    if startDate_short is None and startDate_long is None:
        startDate = datetime.min
    elif startDate_short is None:
        startDate = startDate_long
    else:
        startDate = startDate_short
    stats = list(freq_collection.find({"time_asked": {"$gte": startDate, "$lte": endDate}}))
    stats = json.loads(json_util.dumps(stats))
    return stats

"""
Test 1: DEFAULT VIEW
GET request: http://127.0.0.1:8000/general_stats/
"""

@app.get("/feedback_stats/")
async def success_rate(endDate: datetime = datetime.now(), startDate: datetime = (datetime.now() - timedelta(days=30))):
    db = client.freq_question_db
    freq_collection = db.cds_frequency
    total_questions = freq_collection.count_documents({"time_asked": {"$gte": startDate, "$lte": endDate}})
    successful_questions = freq_collection.count_documents({"time_asked": {"$gte": startDate, "$lte": endDate}, "user_feedback": {"$in": [ "HELPFUL", "NO_FEEDBACK" ] }})
    success_rate = successful_questions / total_questions * 100 if total_questions > 0 else 0
    return {"total_questions": total_questions, "successful_questions": successful_questions, "success_rate": success_rate}

@app.get("/intent_stats/")
async def top_categories(endDate: datetime = datetime.now(), startDate: datetime = (datetime.now() - timedelta(days=30))):
    db = client.freq_question_db
    freq_collection = db.cds_frequency
    pipeline = [
        {"$match": {"time_asked": {"$gte": startDate, "$lte": endDate}}},
        {"$group": {"_id": "$intent", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    intent_stats = list(freq_collection.aggregate(pipeline))
    intent_stats = json.loads(json_util.dumps(intent_stats))
    return {"intent_stats": intent_stats}


""""
AUTHENTICATION API. Code reference from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
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
   


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

#decrypt the token and verify the validity of the token, return the admin's username
async def verifyToken(token : Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        if token == None:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # print("GOT USERNAME", username)
        if username is None:
            raise credentials_exception
        isAdmin = authenticationManager.checkIsAdmin(username)
        if isAdmin:
            return username
        else:
            raise credentials_exception
    except JWTError:

        raise credentials_exception


@app.get("/admins")
async def getAdmins(request : Request):
    token = getToken(request)
    await verifyToken(token)
    adminList = authenticationManager.getAdmins()
    return adminList


@app.post("/add_admin")
async def addAdmin(request : Request):
    jsonData = await request.json()
    usernameToAdd = jsonData["username"]

    token = getToken(request)
    currentUser = await verifyToken(token)
    authenticationManager.addAdmin(currentUser, usernameToAdd)
    return {}


@app.post("/transfer_root_access")
async def transferRootAccess(request : Request):
    jsonData = await request.json()
    transferFrom = jsonData["transferFrom"]
    transferTo = jsonData["transferTo"]
    transferSuccess = authenticationManager.transferRootAcess(transferFrom, transferTo)
    if not transferSuccess:
         raise credentials_exception
    else:
        return {}

    # token = getToken(request)
    # currentUser = await verifyToken(token)
    # isRoot = authenticationManager.checkIsRoot(currentUser)
    # if isRoot:
    #     authenticationManager.addAdmin(usernameToAdd)
   



@app.delete("/delete_user")
async def deleteUser(request : Request):
    jsonData = await request.json()
    userToDelete = jsonData["username"]
    token = getToken(request)
    currentUser =await verifyToken(token)
    authenticationManager.deleteUser(currentUser, userToDelete)
    return {}

@app.get("/currentUser")
async def getCurrentUser(request : Request):
    token = getToken(request)
    username = await verifyToken(token)
    userData = authenticationManager.getUserData(username)
    if userData == None:
        raise credentials_exception
    
    else:
        return userData


# helper methods
def getToken(request : Request):
    if AUTHORIZATION_HEADER_KEY in request.headers:
        return request.headers[AUTHORIZATION_HEADER_KEY]
    else:
        return None
    


from fastapi import BackgroundTasks
isTraining = False

async def sendTrainSignal(questionId, entities, conversationId):
    async with aiohttp.ClientSession() as session:
        global isTraining
        isTraining = True
        response = await rasaCommunicator.injectIntent(EVENT_OCCURED_KEY, entities, session, conversationId)
        print(response)
        unansweredQuestionDbConnector.updateTrainedStatus(questionId, True)
        

# This will be called by the rasa action server to tell the server training is done.
@app.post("/training_done")
async def trainingDone():
    global isTraining
    print("TRAINING DONE")
    isTraining = False
    
@app.get("/training_status")
async def getTrainingStatus():
    global isTraining
    return {"isTraining": isTraining}

@app.post("/train_knowledgebase")
async def trainKnowledgebase(request : Request, background_tasks: BackgroundTasks):
    """
    request body: {"ids":[""]}
    """
    requestJson = await request.json()
    ids = requestJson["ids"]
    entities ={"eventType":"train", "feedback":[]}
    for id in ids:
        questionObj = unansweredQuestionDbConnector.getQuestionAnswerObjectById(id)
        entities["feedback"].append(questionObj)
        conversationId = "random"
        try:
            # async with aiohttp.ClientSession() as session:
            #     response = await rasaCommunicator.injectIntent(EVENT_OCCURED_KEY, entities, session, conversationId)
            #     print(response)
            
            # unansweredQuestionDbConnector.updateTrainedStatus(id, True)
            # return {"success":True}
            background_tasks.add_task(sendTrainSignal,id, entities, conversationId)
            
            return {"success": True}
        except Exception:
            raise HTTPException(status_code=500, detail="change failed")
    
