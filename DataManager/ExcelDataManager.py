from DataManager.DataManager import DataManager
from Data_Ingestion.ExcelProcessor import ExcelProcessor
from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.NotEnoughInformationException import NotEnoughInformationException

"""
DataManager subclass that can handle excel file as data resource and retrieve sparse matrices as pandas dataframes.
"""
class ExcelDataManager(DataManager):
    def __init__(self, filePath, topicToParse =["enrollment"]):
        super().__init__()
        self.topicToParse = topicToParse
        self.excelProcessor = ExcelProcessor(filePath, self.topicToParse)

    """
    See docuementation in DataManager.py
    """
    def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow: Exception) :
        fileNameByYear = start+"_"+end
     
        if not fileNameByYear in self.excelProcessor.getData():
            raise exceptionToThrow

        data = self.excelProcessor.getData()
        dataForEachTopic = data[fileNameByYear]
        if not intent in dataForEachTopic.keys() or dataForEachTopic[intent] is []:
            raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end))
        sparseMatricesForTopic = dataForEachTopic[intent]
        return sparseMatricesForTopic


    """
    See docuementation in DataManager.py
    """
    def getMostRecentYearRange(self):
        def sortFunc(e):
            yearRange = e.split("_")
            startYear= int(yearRange[0])
            return startYear

        years = list(self.excelProcessor.getData().keys())
        years.sort(key = sortFunc, reverse= True)
        mostRecentYearRange = years[0].split("_")

        return (mostRecentYearRange[0], mostRecentYearRange[1])

