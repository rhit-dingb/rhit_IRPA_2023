
from typing import Dict, List
from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import json
import sys
import re
<<<<<<< HEAD
from datetime import datetime, date, timedelta
=======
import aiohttp
import asyncio
from datetime import datetime, date
>>>>>>> winter_iteration_5_available_options

from DataType import DataType
from abc import ABC, abstractmethod
from enum import Enum

sys.path.append('../')

from fastapi import FastAPI, Request, HTTPException
from Parser.RasaCommunicator import RasaCommunicator
from DataManager.constants import DEFINITION
from DataManager.constants import CDS_DEFINITION_DATABASE_NAME
from Parser.JsonDataLoader import JsonDataLoader
from DataManager.constants import CDS_DATABASE_NAME_TEMPLATE
from DataManager.MongoDataManager import MongoDataManager
from Parser.MongoDBSparseMatrixDataWriter import MongoDBSparseMatrixDataWriter
from Parser.ParserFacade import ParserFacade
from Parser.DataLoader import DataLoader
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from fastapi.middleware.cors import CORSMiddleware
from DataManager.constants import ANNUAL_DATA_REGEX_PATTERN, DEFINITION_DATA_REGEX_PATTERN



mongoDbDataManager = MongoDataManager()
rasaCommunicator = RasaCommunicator()
client = MongoClient(MONGO_DB_CONNECTION_STRING)
app = FastAPI()

#A list of allowed origins
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    print("UPLOAD DATA")
    jsonData = await request.json()
    # dataType = jsonData["type"]
    excelData = jsonData["data"]
    # print(jsonData)
    jsonCdsLoader = JsonDataLoader()
    outputName = ""
    if "dataName" in jsonData:
        outputName = jsonData["dataName"]

    if not outputName == "":
        # try:
        # print(excelData)
        print(outputName)
        jsonCdsLoader.loadData(excelData)
        dataWriter = MongoDBSparseMatrixDataWriter(outputName)
        parserFacade = ParserFacade(dataLoader=jsonCdsLoader, dataWriter=dataWriter)
        await parserFacade.parse()
        return {"message": "Done", "uploadedAs": outputName}
        # except Exception:
        #     raise HTTPException(status_code=500, detail="Something went wrong while parsing the input data")

    

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
    try:
        toDelete = jsonData["dataName"]
        didDelete = mongoDbDataManager.deleteData(toDelete)
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
    db = client.freq_question_db
    questions_collection = db.unans_question
    unanswered_questions = list(questions_collection.find({'is_addressed': False}))
    print("DATA FOUND")
    unanswered_questions = json.loads(json_util.dumps(unanswered_questions))
    print(unanswered_questions)
    return unanswered_questions


@app.put("/question_update/{id}")
async def handle_post_answer(id: str, answer: str):
    db = client.freq_question_db
    questions_collection = db.unans_question
    boo1 = questions_collection.update_one({'_id': ObjectId(id)}, {'$set': {'is_addressed': True}})
    boo2 = questions_collection.update_one({'_id': ObjectId(id)}, {'$set': {'answer': answer}})
    if boo1 and boo2:
        return {'message': 'update successfull'}
    else:
        return {'message': 'errors occurred while updating'}

@app.delete("/question_delete/{id}")
async def handle_delete_answer(id: str):
    db = client.freq_question_db
    questions_collection = db.unans_question
    boo1 = questions_collection.delete_one({'_id': ObjectId(id)})
    if boo1:
        return {'message': 'question is successfull deleted'}
    else:
        return {'message': 'question maybe not found and issue occurred'}

@app.post("/question_add/{content}")
async def handle_add_question(content: str):
    db = client.freq_question_db
    questions_collection = db.unans_question
    boo1 = questions_collection.insert_one({
        "content": content,
        "post_date": datetime.today(),
        "is_addressed": False,
        "answer": None})
    if boo1:
        return {'message': 'question is successfull added'}
    else:
        return {'message': 'errors occurred during question add'}

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
async def handle_new_event(intent: QuestionCategory, feedback: UserFeedback, timeAsked: datetime, content: str):
    db = client.freq_question_db
    freq_collection = db.cds_frequency
    if(len(list(freq_collection.find({"question_asked": content}))) == 0):
        boo1 = freq_collection.insert_one({
            "intent": intent.value,
            "user_feedback": feedback.value,
            "time_asked": timeAsked,
            "question_asked": content})
        if boo1:
            return {'message': 'data successfully inserted'}
        else:
            return {'message': 'errors occurred'}
    else:
        boo2 = freq_collection.update_one({'time_asked': timeAsked}, {'$set': {'user_feedback': feedback.value}})
        if boo2:
            return {'message': 'data successfully updated'}
        else:
            return {'message': 'errors occurred'}

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


