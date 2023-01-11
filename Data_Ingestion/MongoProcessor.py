
import pandas as pd
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from DataManager.constants import DATABASE_SPARSE_MATRIX_ROWS_KEY, DATABASE_SPARSE_MATRIX_SUBSECTION_KEY
from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.NoDataFoundException import NoDataFoundException
from DataManager.constants import QUESTION_COLUMN_KEY


class MongoProcessor():
    def __init__(self):
        pass
        # self.data : dict[str, dict[str, TopicData]] = []
        #print(self.data['2020_2021']["high_school_units"].sparseMatrices)
        
    # def getData(self) -> TopicData:
    #     return self.data

    """ 
    
    """ 
    def getSparseMatricesByDbNameAndIntent(self, client, intent, dbName):
        # yearToData = dict()

        # for db_name in db.list_database_names():
            # if(db_name != 'admin' and db_name != 'config' and db_name != 'local'):
        cur_db = client[dbName]
        # data = dict()
            #xl = pd.DataFrame.from_dict(cur_db) #convert current database to Panda DataFrame                            
        # for topic in topicToParse:
        topicData = self.getAllSparseMatrixForTopic(intent, cur_db)
            # get the year key. !!! Assume current standart is CDS_xxxx_xxxx
            # yearKey = db_name[-9:-5]+"_"+db_name[-4:]
                #print('yearkey is  ' + yearKey)
        # yearToData[yearKey] = data

        return topicData     
   

       

    """ 
    Given a topic, this function will find all the sparse matrix for a topic. Currently it is getting it from excel file, but 
    we can swap out for database easily.

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
                questions = []
                for sparseMatrixData in cursor:
                    subsection = sparseMatrixData.get(DATABASE_SPARSE_MATRIX_SUBSECTION_KEY)
                    rows = sparseMatrixData.get(DATABASE_SPARSE_MATRIX_ROWS_KEY)
                    for row in rows:
                        # if QUESTION_COLUMN_KEY in row:
                        questions.append(row[QUESTION_COLUMN_KEY])
                        del row[QUESTION_COLUMN_KEY]
                    df = pd.DataFrame.from_dict(rows)
                    # print(df.head())
                    sparseMatrix = SparseMatrix(subsection, df, questions)
                    topicData.addSparseMatrix(subsection, sparseMatrix)

                return topicData  

        # If nothing found, return empty topic data        
        return topicData
                