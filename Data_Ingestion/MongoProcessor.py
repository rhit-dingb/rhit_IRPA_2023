
from typing import List
import pandas as pd
from Data_Ingestion.DataProcessor import DataProcessor
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from DataManager.constants import DATABASE_SPARSE_MATRIX_ROWS_KEY, DATABASE_SPARSE_MATRIX_SUBSECTION_KEY
from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.NoDataFoundException import NoDataFoundException
from DataManager.constants import QUESTION_COLUMN_KEY
from DataManager.constants import DATABASE_METADATA_FIELD_KEY
from DataManager.constants import DATABASE_QUESTION_ANSWERS_KEY
from Data_Ingestion.SubsectionQnA import SubsectionQnA
from pymongo import MongoClient

class MongoProcessor(DataProcessor):
    """
    Class used by MongoDataManager to retrieve data. This class can be decorated to convert the data retrieved from Mongo DB to different internal
    data models.
    """

    async def getDataByDbNameAndSection(self, client : MongoClient, section : str, dbName : str ) -> List[SubsectionQnA]:
        """
        This function retrieve all the subsection and the data for each subsection given the section into the SubsectionQnA data model.
        :param client: Mongo client to make request to MongoDB.
        :param section: section to retrieve data for
        :param dbName: database name to retrieve the section for
        :return: List of SubsectionQnA
        """
        cur_db = client[dbName]
        subsectionsQnAList = []
        for name in cur_db.list_collection_names():
            if section == name:
                cursor = cur_db[name].find({})
                for data in cursor:
                    subsection = data.get(DATABASE_SPARSE_MATRIX_SUBSECTION_KEY)
                    questionAnswer = data.get(DATABASE_QUESTION_ANSWERS_KEY)
                    metadata = data.get(DATABASE_METADATA_FIELD_KEY)
                    subsectionQnA = SubsectionQnA(subsection, questionAnswer, metadata)
                    subsectionsQnAList.append(subsectionQnA)

        return subsectionsQnAList
    
