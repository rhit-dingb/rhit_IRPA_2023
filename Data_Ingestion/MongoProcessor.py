
import pandas as pd
from Data_Ingestion.SparseMatrix import SparseMatrix

from Data_Ingestion.TopicData import TopicData



class MongoProcessor():
    def __init__(self, topicToParse):
        self.data : dict[str, dict[str, TopicData]] = []
        #print(self.data['2020_2021']["high_school_units"].sparseMatrices)
        
    def getData(self) -> TopicData:
        return self.data

    """ 
    return from MongoDB collection into dictionary
    """ 
    def processCollectiontoSparseMatrix(self, topicToParse):
        #yearToData = dict()
        cursor = topicToParse.find()
        list_dic = list(cursor)
        #print(list_dic)
        self.data = list_dic
        return True

    # """ 
    # Given a topic, this function will find all the sparse matrix for a topic. Currently it is getting it from excel file, but 
    # we can swap out for database easily.

    # PARAMETERS: 
    
    # topic: the topic to get the sparse matrix for

    # dataSourceConnector: excel connector from pandas that we can use to retrieve data.

    # Returns: TopicData class.
    # """
    # def getAllSparseMatrixForTopic(self, topic, dataSourceConnector) -> TopicData:
        
    #     seperator = "_"
        
    #     topicData = TopicData(topic)
    #     #put this here for now
    #     topic = topic.replace("_", " ")
        
    #     for name in dataSourceConnector.sheet_names:
    #         topic_key_words = [x.lower() for x in name.split(seperator)]
            
   
    #         # for each sheet, the name has to be in the format subsection_topic. For example: race_enrollment
    #         if topic in topic_key_words:
    #             #Assume the naming convention is: Section_Subsection
    #             subsectionName = topic_key_words[len(topic_key_words)-1]
    #             df = dataSourceConnector.parse(name)
    #             sparseMatrix = SparseMatrix(subsectionName, df)
    #             topicData.addSparseMatrix(subsectionName, sparseMatrix)
    #     return topicData  
                