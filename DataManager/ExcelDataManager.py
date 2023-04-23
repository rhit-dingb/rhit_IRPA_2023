import re
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
DataManager subclass that can handle excel file as data resource-- used for only testing purposes.
"""
class ExcelDataManager(DataManager):
    def __init__(self, filePath):
        super().__init__()
        self.excelProcessor = ExcelProcessor(filePath)

    async def getDataBySection(self, section, exceptionToThrow, startYear = None, endYear = None ):
        section = section.replace("_", " ")
        yearKey = startYear+"_"+endYear
     
        if not yearKey in self.excelProcessor.getData():
            raise exceptionToThrow

        data = self.excelProcessor.getData()
        dataForEachTopic = data[yearKey]
       
        
        if not section in dataForEachTopic.keys():
            
            raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = section, start= startYear, end=endYear), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
            
        topicData : TopicData = dataForEachTopic[section]

        if not topicData.hasData():
            raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = section, start= startYear, end=endYear), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
        
        return topicData
    
    # async def getDataByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow: Exception) -> TopicData:
    #     yearKey = start+"_"+end
     
    #     if not yearKey in self.excelProcessor.getData():
    #         raise exceptionToThrow

    #     data = self.excelProcessor.getData()
    #     dataForEachTopic = data[yearKey]
       
        
    #     if not intent in dataForEachTopic.keys():
            
    #         raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent.replace("_", " "), start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
            
    #     topicData : TopicData = dataForEachTopic[intent]

    #     if not topicData.hasData():
    #         raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent.replace("_", " "), start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
        
    #     return topicData

    def getMostRecentYearRange(self) -> Tuple[str, str] :
        def sortFunc(e):
            yearRange = e.split("_")
            startYear= int(yearRange[0])
            return startYear

        years = list(self.excelProcessor.getData().keys())
        years.sort(key = sortFunc, reverse= True)
        mostRecentYearRange = years[0].split("_")

        return (mostRecentYearRange[0], mostRecentYearRange[1])


     
    def getAvailableOptions(self,intent, startYear, endYear):
        pass

    
    def deleteData(self, dataName) -> bool:
        pass

    
    def getAllSubsectionForSection(self, section, startYear=None, endYear=None):
        pass

    
    def getSectionAndSubsectionsForData(self,dataName, filter=lambda x: True):
        pass
    
    
    def getAllAvailableData(self, regex : re.Pattern):
        pass
        

     
    def findAllYearAngosticDataName(self):
        return []

    
    def getAllAvailableYearsSorted(self):
        pass

    
    def getAvailableDataForSpecificYearRange(self, startYear, endYear):
        pass

    
    def getSections(self, dataName):
        pass
