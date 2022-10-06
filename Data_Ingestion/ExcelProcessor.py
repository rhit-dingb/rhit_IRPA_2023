
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


    # This function will get all the sparse matrices 
    # numbers: sequence or iterable, all the elements must be numbers
    # Returns the sum of all the numbers in the sequence or iterable
    # Throws ArithmeticError if any of the element is not a number
    def getAllSparseMatrixForTopic(self, topic, dataSourceConnector):
        sparseMatrices = []
        for name in dataSourceConnector.sheet_names:
            topic_key_words = [x.lower() for x in name.split("_")]
            if topic in topic_key_words:
                df = dataSourceConnector.parse(name)
                sparseMatrices.append(df)

        return sparseMatrices    
                