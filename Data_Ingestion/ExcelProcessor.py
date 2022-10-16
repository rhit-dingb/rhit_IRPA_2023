
import pandas as pd

class ExcelProcessor():
    def __init__(self):
        pass

  
    def processExcelSparse(self, path, topicToParse):
        data = dict()
        xl = pd.ExcelFile(path)
        for topic in topicToParse:
            data[topic] = self.getAllSparseMatrixForTopic(topic, xl)

        return data

    """ 
    Given a topic, this function will find all the sparse matrix for a topic. Currently it is getting it from excel file, but 
    we can swap out for database easily.
    topic: the topic to get the sparse matrix for
    dataSourceConnector: some sort of connector that we can use to retrieve data.
    Returns: a list of sparse matrix represented by pandas dataframe.
    """
    def getAllSparseMatrixForTopic(self, topic, dataSourceConnector):
        sparseMatrices = []
        for name in dataSourceConnector.sheet_names:
            topic_key_words = [x.lower() for x in name.split("_")]
            if topic in topic_key_words:
                df = dataSourceConnector.parse(name)
                sparseMatrices.append(df)

        return sparseMatrices    
                