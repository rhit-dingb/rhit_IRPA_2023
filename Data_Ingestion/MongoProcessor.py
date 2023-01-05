
import pandas as pd
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData


class MongoProcessor():
    def __init__(self):
        pass
        # self.data : dict[str, dict[str, TopicData]] = []
        #print(self.data['2020_2021']["high_school_units"].sparseMatrices)
        
    # def getData(self) -> TopicData:
    #     return self.data

    """ 
    return from MongoDB collection into dictionary
    """ 
    def processCollectiontoSparseMatrix(self, db, topicToParse, yearKey):
        # yearToData = dict()

        # for db_name in db.list_database_names():
            # if(db_name != 'admin' and db_name != 'config' and db_name != 'local'):
        cur_db = db[yearKey]
        # data = dict()
            #xl = pd.DataFrame.from_dict(cur_db) #convert current database to Panda DataFrame                            
        # for topic in topicToParse:
        topicData = self.getAllSparseMatrixForTopic(topicToParse, cur_db)
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
            #Might be better if we send a databse query, but it should be okay.
            topic_key_words = [x.lower() for x in name.split(seperator)]
            # for each sheet, the name has to be in the format subsection_topic. For example: race_enrollment
            if topic in topic_key_words:
                #Assume the naming convention is: Section_Subsection
                subsectionName = topic_key_words[len(topic_key_words)-1]
                df = pd.DataFrame.from_dict(curDB[name].find({}))
                sparseMatrix = SparseMatrix(subsectionName, df)
                topicData.addSparseMatrix(subsectionName, sparseMatrix)
        return topicData  
                