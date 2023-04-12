
from typing import List
import pandas as pd
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


class MongoProcessor():
    def __init__(self):
        pass

    async def getDataByDbNameAndSection(self, client, section, dbName) -> List[SubsectionQnA]:
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
    

 
    def getSparseMatricesByDbNameAndIntent(self, client, intent, dbName):
        cur_db = client[dbName]

        topicData = self.getAllSparseMatrixForTopic(intent, cur_db)
    
        return topicData     
          

    """ 
    Given a topic, this function will find all the sparse matrix for a topic. 
    PARAMETERS: 
    
    topic: the topic to get the sparse matrix for

    dataSourceConnector: excel connector from pandas that we can use to retrieve data.

    Returns: TopicData class.
    """
    def getAllSparseMatrixForTopic(self, topic, curDB) -> TopicData:    
        seperator = "_"
        topicData = TopicData(topic)
        #put this here for now
        topic = topic.replace("_", " ")
        for name in curDB.list_collection_names():
            # topic_key_words = [x.lower() for x in name.split(seperator)]
            # for each sheet, the name has to be in the format subsection_topic. For example: race_enrollment
            # print("CHECKING")
            # # print(name)
            # print(name, topic, topic == name)
            
            if topic == name:
                cursor = curDB[name].find({})
                # print("CURSOR")
                # print(cursor[0])
               
                for sparseMatrixData in cursor:
                    questions = []
                    subsection = sparseMatrixData.get(DATABASE_SPARSE_MATRIX_SUBSECTION_KEY)
                    rows = sparseMatrixData.get(DATABASE_SPARSE_MATRIX_ROWS_KEY)
                    metadata = sparseMatrixData.get(DATABASE_METADATA_FIELD_KEY)
                    for row in rows:
                        questions.append(row[QUESTION_COLUMN_KEY])
                        del row[QUESTION_COLUMN_KEY]
                    df = pd.DataFrame.from_dict(rows)
                    # print(df.head())
                    # print(questions)
                    # print("GOT METADATA")
                    # print(metadata)
                    sparseMatrix = SparseMatrix(subsection, df,  metadata=metadata, questions = questions,)
                    topicData.addSparseMatrix(subsection, sparseMatrix)

                return topicData  

    #     # If nothing found, return empty topic data        
    #     return topicData
                