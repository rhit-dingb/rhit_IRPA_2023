from typing import Tuple
from DataManager.DataManager import DataManager
from Data_Ingestion.ExcelProcessor import ExcelProcessor
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.NotEnoughInformationException import NotEnoughInformationException
from Exceptions.ExceptionTypes import ExceptionTypes
"""
DataManager subclass that can handle excel file as data resource.
"""
class ExcelDataManager(DataManager):
    def __init__(self, filePath, topicToParse =["enrollment"]):
        super().__init__()
        self.topicToParse = topicToParse
        self.excelProcessor = ExcelProcessor(filePath, self.topicToParse)

    """
    See docuementation in DataManager.py
    """
    def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow: Exception) -> TopicData:
        yearKey = start+"_"+end
     
        if not yearKey in self.excelProcessor.getData():
            raise exceptionToThrow

        data = self.excelProcessor.getData()
        dataForEachTopic = data[yearKey]
       
        
        if not intent in dataForEachTopic.keys():
            raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
            
        topicData : TopicData = dataForEachTopic[intent]

        
        if not topicData.hasData():
            raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
        
        return topicData


    """
    See docuementation in DataManager.py
    """
    def getMostRecentYearRange(self) -> Tuple[str, str] :
        def sortFunc(e):
            yearRange = e.split("_")
            startYear= int(yearRange[0])
            return startYear

        years = list(self.excelProcessor.getData().keys())
        years.sort(key = sortFunc, reverse= True)
        mostRecentYearRange = years[0].split("_")

        return (mostRecentYearRange[0], mostRecentYearRange[1])

