from typing import List
from pymongo import MongoClient
from DataManager.constants import MONGO_DB_CONNECTION_STRING
import json
from bson import json_util
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from UnansweredQuestions.constants import DB_UNANSWERED_QUESTION_DATE_FIELD_KEY


class MongoDBUnansweredQuestionConnector():
    def __init__(self):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        self.db = self.client.freq_question_db
        self.questions_collection =  self.db.unans_question

    def getAllUnansweredQuestionAndAnswer(self):
        # fieldToGetBody = {}
        # for field in fieldsToGet:
        #     fieldToGetBody[field] = 1
        # unanswered_questions = list(questions_collection.find({'is_addressed': False}))
        unanswered_questions = list(self.questions_collection.find({}))
        unanswered_questions = json.loads(json_util.dumps(unanswered_questions))
        # print("GETTING QUESTIOS")
        # print(unanswered_questions)
        return unanswered_questions


    def getAnsweredQuestionSortedByDate(self):
        unanswered_questions = self.questions_collection.find({'is_addressed': True}).sort([(DB_UNANSWERED_QUESTION_DATE_FIELD_KEY, pymongo.ASCENDING), ("_id", pymongo.ASCENDING)])
        return unanswered_questions


    def provideAnswerToUnansweredQuestion(self, id: str, answer: str):
        boo1 = self.questions_collection.update_one({'_id': ObjectId(id)}, {'$set': {'is_addressed': True}})
        boo2 = self.questions_collection.update_one({'_id': ObjectId(id)}, {'$set': {'answer': answer}})
        if boo1 and boo2:
            return {'message': 'update successfull'}
        else:
            return {'message': 'errors occurred while updating'}

    def addNewUnansweredQuestion(self, question : str, chatbotAnswers : List[str]):
        unansweredQuestions = self.getAllUnansweredQuestionAndAnswer()
        for questionInDB in unansweredQuestions: 
       
            if question.lower() == questionInDB["content"].lower():
                print("QUESTION ALREADY EXIST")
                return  {'message': 'questionExist'}
        
        toAdd = {
            "content": question,
            "post_date": datetime.today(),
            "is_addressed": False,
            "chatbotAnswers": chatbotAnswers,
            "answer": None}
        
        boo1 = self.questions_collection.insert_one(toAdd)
     
        if boo1:
            print("QUESTION ADDED SUCCESSFULLY")
            print(toAdd)
            return {'message': 'question is successfull added'}
        else:
            print("ERROR OCCURED DURING QUESTION ADD")
            return {'message': 'errors occurred during question add'}

    
    def getQuestionAnswerObjectById(self, id):
       return json.loads(json_util.dumps(self.questions_collection.find_one({'_id': ObjectId(id)})))