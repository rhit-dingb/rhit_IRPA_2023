from typing import Tuple
from DataManager.DataManager import DataManager
#from Data_Ingestion.ExcelProcessor import ExcelProcessor
# from Data_Ingestion.SparseMatrix import SparseMatrix
# from Data_Ingestion.TopicData import TopicData
# from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
# from Exceptions.NoDataFoundException import NoDataFoundException
# from Exceptions.NotEnoughInformationException import NotEnoughInformationException
# from Exceptions.ExceptionTypes import ExceptionTypes
import json
import pymongo
from pymongo import MongoClient
"""
MongoDataManager subclass that can handle connections with MongoDB data
"""

class MongoDataManager(DataManager):
    def __init__(self, topicToParse = ["enrollment"]):
        super().__init__()
        self.topicToParse = topicToParse
        #self.MongoProcessor = MongoProcessor(filePath, self.topicToParse)

print("Started!")
DATABASE_PRENAME = "CDS_"

client = MongoClient('mongodb://localhost:27017')
db = client["CDS_2020-2021"]
INTENTION_LIST = db.list_collection_names()
print(INTENTION_LIST)
collection = db.Enrollment_General
cursor = collection.find({"undergraduate": 1})
# for doc in cursor:
#     print(doc)

def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow: Exception) -> TopicData:
        yearKey = DATABASE_PRENAME+start+"-"+end
        if not yearKey in self.excelProcessor.getData():
            raise exceptionToThrow
        data = self.excelProcessor.getData()
        dataForEachTopic = data[yearKey]

        if not intent in dataForEachTopic.keys():
            raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
            
        topicData : TopicData = dataForEachTopic[intent]
        
        if not topicData.hasData():
            raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
        
        return topicData