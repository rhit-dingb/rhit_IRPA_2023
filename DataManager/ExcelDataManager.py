from DataManager.DataManager import DataManager
from Data_Ingestion.ExcelProcessor import ExcelProcessor

"""
DataManager subclass that can handle excel file as data resource and retrieve sparse matrices as pandas dataframes.
"""
class ExcelDataManager(DataManager):
    def __init__(self, filePath):
        super().__init__()
        self.topicToParse = ["enrollment"]
        self.excelProcessor = ExcelProcessor(filePath, self.topicToParse)

    """
    See docuementation in DataManager.py
    """
    def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end):
        fileNameByYear = start+"_"+end
        if not fileNameByYear in self.excelProcessor.getData():
             raise Exception("No data found for given year range {start}-{end}".format(start = start, end = end))

        data = self.excelProcessor.getData()
        dataForEachTopic = data[fileNameByYear]
        sparseMatricesForTopic = dataForEachTopic[intent]
        return sparseMatricesForTopic


    """
    See docuementation in DataManager.py
    """
    def getMostRecentYearRange(self):
        def sortFunc(e):
            yearRange = e.split("_")
            endYear = yearRange[0]
            return endYear

        years = list(self.excelProcessor.getData().keys())
        years.sort(key = sortFunc)
        mostRecentYearRange = years[0].split("_")
        return (mostRecentYearRange[0], mostRecentYearRange[1])

