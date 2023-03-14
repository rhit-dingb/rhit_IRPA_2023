
import json
from typing import Dict, List, Tuple
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from Parser.DataWriter import DataWriter
from Data_Ingestion.SparseMatrix import SparseMatrix
from pymongo import MongoClient
from DataManager.constants import DATABASE_SUBSECTION_FIELD_KEY
from Parser.QuestionAnswer import QuestionAnswer
from DataManager.constants import DATABASE_METADATA_FIELD_KEY
from DataManager.constants import DATABASE_QUESTION_ANSWERS_KEY

class MongoDbNoChangeDataWriter(DataWriter):
    def __init__(self, outputName):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        self.databaseName = outputName
        self.db = self.client[self.databaseName]
       


    def write(self, sectionToQuestionAnswer : Dict[str, List[Tuple[str,  List[QuestionAnswer]]]]):
        sectionsInserted = []
       
        for sectionKey in sectionToQuestionAnswer:
            dataForEachSubSection = sectionToQuestionAnswer[sectionKey]
            subsectionsInserted = []
            for data in dataForEachSubSection: 
                subsection, subsectionQuestionAnswers = data
              
                body = dict()
                metadata = dict()
                for questionAnswer in subsectionQuestionAnswers:
                   if questionAnswer.isMetaData:
                       metadata[questionAnswer.getQuestion()] = questionAnswer.getAnswer()
                   else:
                        body[questionAnswer.getQuestion()] = questionAnswer.getAnswer()

                self.db[sectionKey].update_one({DATABASE_SUBSECTION_FIELD_KEY : subsection}, {
                    "$set": {
                        DATABASE_QUESTION_ANSWERS_KEY : body,
                        DATABASE_SUBSECTION_FIELD_KEY : subsection,
                        DATABASE_METADATA_FIELD_KEY: metadata
                    }
                }, upsert=True )
                subsectionsInserted.append(subsection)
                
            query = { DATABASE_SUBSECTION_FIELD_KEY : { "$nin": subsectionsInserted } }
            self.db[sectionKey].delete_many(query)
            sectionsInserted.append(sectionKey)

        # duplicate code 
        collections =  self.db.list_collection_names()
        for collection in collections:
            if not collection in sectionsInserted:
                self.db[collection].drop()
        
                

