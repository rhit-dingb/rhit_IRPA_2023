from typing import Tuple
from DataManager.DataManager import DataManager
from Data_Ingestion.ExcelProcessor import ExcelProcessor
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.NotEnoughInformationException import NotEnoughInformationException
from Exceptions.ExceptionTypes import ExceptionTypes
import json
from pymongo import MongoClient
"""
MongoDataManager subclass that can handle connections with MongoDB data
"""
DATABASE_PRENAME = "CDS_"

class MongoDataManager():
    def __init__(self, topicToParse = ["enrollment"]):
        super().__init__()
        self.topicToParse = topicToParse
        #self.MongoProcessor = MongoProcessor(filePath, self.topicToParse)
        self.client = MongoClient('mongodb://localhost:27017')

    print("Started!")
    
    client = MongoClient('mongodb://localhost:27017')
    db = client["CDS_2020-2021"]
    # INTENTION_LIST = db.list_collection_names()
    # print(INTENTION_LIST)
    # collection = db.Enrollment_General
    # cursor = collection.find({"undergraduate": 1})
    # for doc in cursor:
    #     print(doc)

    """
    See docuementation in DataManager.py
    """
    def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow: Exception) -> TopicData:
            yearKey = DATABASE_PRENAME + str(start) + "-" + str(end)
            if not yearKey in self.client.list_database_names():
                raise exceptionToThrow
            db= self.client[yearKey]

            if not intent in db.list_collection_names():
                raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
                
            topicData : TopicData = db[intent]
            # cursor = topicData.find()
            # for doc in cursor:
            #     print(doc)
            return topicData


# -----------The following are Unit Tests for the MongoDataManager Class
NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT = "Sorry I could not find any data for academic year {start}-{end}"
exceptionToThrow = NoDataFoundException(NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=2020, end=2021), ExceptionTypes.NoDataFoundForAcademicYearException)
manager = MongoDataManager()
manager.getSparseMatricesByStartEndYearAndIntent("Enrollment_General",2020,2021,exceptionToThrow)
