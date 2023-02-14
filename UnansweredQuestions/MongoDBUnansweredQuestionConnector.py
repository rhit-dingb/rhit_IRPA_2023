from pymongo import MongoClient
from DataManager.constants import MONGO_DB_CONNECTION_STRING
import json
import sys
from bson import json_util
import pymongo

from UnansweredQuestions.constants import DB_UNANSWERED_QUESTION_DATE_FIELD_KEY

class MongoDBUnansweredQuestionConnector():
    def __init__(self):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)

    def getAllUnansweredQuestionAndAnswer(self):
        pass

    def getAnsweredQuestionSortedByDate(self):
        db = self.client.freq_question_db
        questions_collection = db.unans_question
        unanswered_questions = questions_collection.find({'is_addressed': True}).sort([(DB_UNANSWERED_QUESTION_DATE_FIELD_KEY, pymongo.ASCENDING), ("_id", pymongo.ASCENDING)])
        return unanswered_questions



    def provideAnswerToUnansweredQuestion(questionId):
        pass

    def addNewUnansweredQuestion(question):
        pass

    