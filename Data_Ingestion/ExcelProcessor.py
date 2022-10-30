
import pandas as pd
import os

class ExcelProcessor():
    def __init__(self, path, topicToParse):
        self.data = self.processExcelCDSDataByYearToSparseMatrix(path, topicToParse)

    def getData(self):
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
            
            yearKey = fileNameSplit[len(fileNameSplit)-2]+"_"+fileNameSplit[len(fileNameSplit)-1]
            yearToData[yearKey] = data
        
        return yearToData

    """ 
    Given a topic, this function will find all the sparse matrix for a topic. Currently it is getting it from excel file, but 
    we can swap out for database easily.

    PARAMETERS: 
    
    topic: the topic to get the sparse matrix for

    dataSourceConnector: some sort of connector that we can use to retrieve data.

    Returns: a list of sparse matrix represented by pandas dataframe.
    """
    def getAllSparseMatrixForTopic(self, topic, dataSourceConnector):
        sparseMatrices = []
        for name in dataSourceConnector.sheet_names:
            nameReplace = name.replace("_", " ")
            topic_key_words = [x.lower() for x in nameReplace.split(" ")]
            if topic in topic_key_words:
                df = dataSourceConnector.parse(name)
                df["Value"] = df["Value"].astype(float)
                sparseMatrices.append(df)

        return sparseMatrices    
                