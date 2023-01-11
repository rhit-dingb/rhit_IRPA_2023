
import pandas as pd
import os
from Data_Ingestion.SparseMatrix import SparseMatrix

from Data_Ingestion.TopicData import TopicData



class ExcelProcessor():
    def __init__(self, path, topicToParse):
        self.data : dict[str, dict[str, TopicData]] = self.processExcelSparseMatrixByYearToSparseMatrix(path, topicToParse)
        #print(self.data['2020_2021']["high_school_units"].sparseMatrices)
        
    def getData(self) -> TopicData:
        return self.data

    """ 
    Given a path to the excel file containing sparse matrix for difference cds section for a particular year and a list of topics to parse,
    this method will convert those sparse matrix to panda dataframes and save into the internal sparse matrix data model. 
    
    Returns a dictionary, the key is each section of the cds data, the value is instance of the TopicData, which contains multiple sparse matrix,
    each sparse matrix correspond to a subsection within the section of a cds section. If that section has no subsection, it will have one sparse matrix.
    """ 
    def processExcelSparseMatrixByYearToSparseMatrix(self, path, topicToParse):
        yearToData = dict()
        for fileName in os.listdir(path):
            #Skip these extra files created by excel
            if '~$' in fileName:
                continue

            data = dict()
            xl = pd.ExcelFile(path+"/"+fileName)
            for topic in topicToParse:
                data[topic] = self.getAllSparseMatrixForTopic(topic, xl)

            # The filename must be something like CDSData_2020_2021
            fileNameWithNoExtension = os.path.splitext(fileName)[0]
            fileNameSplit = fileNameWithNoExtension.split("_")
            
            # get the year key.
            yearKey = fileNameSplit[len(fileNameSplit)-2]+"_"+fileNameSplit[len(fileNameSplit)-1]
            yearToData[yearKey] = data
        return yearToData

    """ 
    Given a topic, this function will find all the sparse matrix for a topic. Currently it is getting it from excel file, but 
    we can swap out for database easily.

    PARAMETERS: 
    
    topic: the topic to get the sparse matrix for

    dataSourceConnector: excel connector from pandas that we can use to retrieve data.

    Returns: TopicData class.
    """
    def getAllSparseMatrixForTopic(self, topic, dataSourceConnector) -> TopicData:
        
        seperator = "_"
        
        topicData = TopicData(topic)
        #put this here for now
        topic = topic.replace("_", " ")
        
        for name in dataSourceConnector.sheet_names:
            topic_key_words = [x.lower() for x in name.split(seperator)]
            
   
            # for each sheet, the name has to be in the format subsection_topic. For example: race_enrollment
            if topic in topic_key_words:
                #Assume the naming convention is: Section_Subsection
                subsectionName = topic_key_words[len(topic_key_words)-1]
                print(subsectionName)
                df = dataSourceConnector.parse(name)
                sparseMatrix = SparseMatrix(subsectionName, df)
                topicData.addSparseMatrix(subsectionName, sparseMatrix)
                
        return topicData  
                