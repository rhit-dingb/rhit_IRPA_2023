from typing import Dict, List
from pymongo import MongoClient
from DataManager.constants import MONGO_DB_CONNECTION_STRING
import json
from bson import json_util
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from UnansweredQuestions.UnasweredQuestionDBConnector import UnansweredQuestionDbConnector
from UnansweredQuestions.constants import DB_UNANSWERED_QUESTION_DATE_FIELD_KEY


class MongoDBUnansweredQuestionConnector(UnansweredQuestionDbConnector):
    def __init__(self):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        self.db = self.client.freq_question_db
        self.questions_collection =  self.db.unans_question

    def getAllUnansweredQuestionAndAnswer(self):
        # fieldToGetBody = {}
        # for field in fieldsToGet:
        #     fieldToGetBody[field] = 1
        # unanswered_questions = list(questions_collection.find({'is_addressed': False}))
        orderToUse = pymongo.DESCENDING
        unanswered_questions = list(self.questions_collection.find({}).sort([(DB_UNANSWERED_QUESTION_DATE_FIELD_KEY, orderToUse), ("_id", pymongo.ASCENDING)]))
        unanswered_questions = json.loads(json_util.dumps(unanswered_questions))
        # print("GETTING QUESTIOS")
        # print(unanswered_questions)
        return unanswered_questions


    def getAnsweredQuestionSortedByDate(self, order="ASCENDING"):
        orderToUse = pymongo.ASCENDING
        if (order=="DESCENDING"):
            orderToUse = pymongo.DESCENDING

        unanswered_questions = self.questions_collection.find({'is_addressed': True}).sort([(DB_UNANSWERED_QUESTION_DATE_FIELD_KEY, orderToUse), ("_id", pymongo.ASCENDING)])
        return unanswered_questions


    def provideAnswerToUnansweredQuestion(self, id: str, answer: str):
        boo1 = self.questions_collection.update_one({'_id': ObjectId(id)}, {'$set': {'is_addressed': True}})
        boo2 = self.questions_collection.update_one({'_id': ObjectId(id)}, {'$set': {'answer': answer}})
        if boo1 and boo2:
            return {'message': 'update successfull'}
        else:
            return {'message': 'errors occurred while updating'}

  
    def addNewUnansweredQuestion(self, question : str, chatbotAnswers : List[Dict[str, any]]):
        """
        Add new unanswered question to the mongodb database, if the unanswered question exist, replace it.
        """  
        # unansweredQuestions = self.getAllUnansweredQuestionAndAnswer()
        # for questionInDB in unansweredQuestions: 
       
        #     if question.lower() == questionInDB["content"].lower():
        #         print("QUESTION ALREADY EXIST")
        #         return  {'message': 'questionExist'}

        toAdd = {
            "content": question,
            "post_date": datetime.today(),
            "is_addressed": False,
            "chatbotAnswers": chatbotAnswers,
            "answer": None,
            "trained": False
            }
        
        boo1 = self.questions_collection.replace_one({"content":question}, toAdd, upsert=True)
        print(boo1)
        return boo1

    def updateFeedbackForAnswer(self, questionId, chatbotAnswer : str, feedback):
     
        filter = {'_id': ObjectId(questionId), "chatbotAnswers":{"$elemMatch": {"answer":chatbotAnswer } }}
        # data = self.questions_collection.find_one(filter)
        # print(json.loads(json_util.dumps(data)))
        toUpdate = {"$set": {"chatbotAnswers.$.feedback": feedback}}
        result = self.questions_collection.update_one(filter, toUpdate)
        print("RESULT")
        print(result)
        modifiedCount = result.modified_count
        if modifiedCount == 1:
            return True
        else:
            return False
    
    def updateTrainedStatus(self, questionId: str, status : bool):
            filter = {'_id': ObjectId(questionId)}
            toUpdate ={"$set": {"trained": status}}
            result = self.questions_collection.update_one(filter, toUpdate)


    def getQuestionAnswerObjectById(self, id):
       return json.loads(json_util.dumps(self.questions_collection.find_one({'_id': ObjectId(id)})))
    

    def deleteUnansweredQuestion(self,id):
        deleteSuccess = self.questions_collection.delete_one({'_id': ObjectId(id)})
        return deleteSuccess