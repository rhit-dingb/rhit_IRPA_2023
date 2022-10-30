
import pandas as pd
import os
from Data_Ingestion.SparseMatrix import SparseMatrix

from Data_Ingestion.TopicData import TopicData



class ExcelProcessor():
    def __init__(self, path, topicToParse):
        self.data : dict[str, dict[str, TopicData]] = self.processExcelCDSDataByYearToSparseMatrix(path, topicToParse)

    def getData(self) -> TopicData:
        return self.data

    def processExcelCDSDataByYearToSparseMatrix(self, path, topicToParse):
        yearToData = dict()
        for fileName in os.listdir(path):
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
        topicData = TopicData(topic)

        for name in dataSourceConnector.sheet_names:
            nameReplace = name.replace("_", " ")

        
            topic_key_words = [x.lower() for x in nameReplace.split(" ")]

            # for each sheet, the name has to be in the format subsection_topic. For example: race_enrollment
            if topic in topic_key_words:
                subsectionName = topic_key_words[0]
                df = dataSourceConnector.parse(name)
                sparseMatrix = SparseMatrix(subsectionName, df)
                topicData.addSparseMatrix(subsectionName, sparseMatrix)

        return topicData  
                