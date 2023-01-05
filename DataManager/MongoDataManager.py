from typing import Tuple
from DataManager.DataManager import DataManager
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.NotEnoughInformationException import NotEnoughInformationException
from Exceptions.ExceptionTypes import ExceptionTypes
import json
from pymongo import MongoClient

from rhit_IRPA_2023.DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
"""
MongoDataManager subclass that can handle connections with MongoDB data
"""


class MongoDataManager():
    def __init__(self):
        super().__init__()
        self.mongoProcessor = MongoProcessor()
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)

    # print("Started!")
    
    # client = MongoClient('mongodb://localhost:27017')
    # dbs = MongoClient().list_database_names()
    # CDS_DB_NAMES = ["CDS_2014-2015","CDS_2019-2020","CDS_2020-2021"]
    #db = client["CDS_2020-2021"]
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
            # TODO: raise exception for this:
            # if not intent in db.list_collection_names():
            #     raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
            #localCollection = db[intent]
            self.mongoProcessor.processCollectiontoSparseMatrix(self.client, intent, yearKey)
            topicData : TopicData = self.mongoProcessor.getData()
            # cursor = topicData.find()
            # for doc in cursor:
            #     print(doc)           
            return topicData

    """
    See docuementation in DataManager.py
    """
    def getMostRecentYearRange(self) -> Tuple[str, str] :
        def sortFunc(e):
            yearRange = e.split("_")
            startYear= int(yearRange[1])
            return startYear

        dbNameWithYears = list(self.client.list_database_names())
        dbNameWithYears.sort(key = sortFunc, reverse= True)
        mostRecentYearRange = dbNameWithYears[0].split("_")
        mostRecentYearRange = mostRecentYearRange

        return (mostRecentYearRange[0], mostRecentYearRange[1])

# -----------The following are Unit Tests for the MongoDataManager Class
# NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT = "Sorry I could not find any data for academic year {start}-{end}"
# exceptionToThrow = NoDataFoundException(NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=2020, end=2021), ExceptionTypes.NoDataFoundForAcademicYearException)
# manager = MongoDataManager()
# manager.getSparseMatricesByStartEndYearAndIntent(["enrollment"],2020,2021,exceptionToThrow)
