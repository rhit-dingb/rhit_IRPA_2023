
from typing import Dict, List, Tuple
# from DataManager.YearDataSelector import YearlyDataSelector
# from DataManager.YearDataSelectorByCohort import YearlyDataSelectorByCohort
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from Exceptions.ExceptionTypes import ExceptionTypes

from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT, NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.ExceptionMessages import NO_DATA_EXIST_MESSAGE

import re
from abc import ABC, abstractmethod

class DataManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def getAvailableOptions(self,intent, startYear, endYear):
        pass
  
    @abstractmethod
    async def getDataBySection(self, section, exceptionToThrow, startYear = None, endYear = None,  databaseFilter = lambda x :True):
        """
            Given the section, start year and end year(i.e. 2020, 2021) of CDS or any other data stored, it will look at all database according to the start year and 
            and end year, finding the first database containing the section. From that selected database, retreive the list of subsections data for the given section. 
            Subsection data can be represented in any way based on the concrete class. The filter parameter can selectively choose which database use.
            :param section: The section to get data from. If startYear and endYear is not given, then subsection for the given section in year agnostic data will be returned
            "parm startYear: Start year of the cds data wanted. Optional
            :param endYear: end year of the cds data we want. Optional
            :param exceptionToThrow: the exception to throw if no data is found.
            :return: Internal data model representing a section's subsection data.
        """  
        pass
 
    @abstractmethod
    def getMostRecentYearRange(self) -> Tuple[str, str]:
        """
        This function will get the most recent year of the data that is currently available. For example:
        if there are 2019-2020 data and 2020-2021 data, it will return a tuple: (2020, 2021)
        """  
        pass
    
    @abstractmethod
    def deleteData(self, dataName : str) -> bool:
        """
        Given a data name, this function will try to delete that data in the datasource. 
        :return: boolean flag representing if deletion was successful or not.
        """  
        pass

    @abstractmethod
    def getAllSubsectionForSection(self, section, startYear=None, endYear=None) -> List[str]:
        """
        Given a section, get all the subsections for that section. If the startYear and endYear is none, Year agnostic data is search on, otherwise yearly 
        data will be searched on based on startYear and endYear.
        :param section: The section to get subsections for. 
        "parm startYear: Start year of the cds data wanted. Optional
        :param endYear: end year of the cds data we want. Optional
        :return: List of subsection names.
        """  
        pass

    @abstractmethod
    def getSectionAndSubsectionsForData(self,dataName, filter=lambda x: True) -> Dict[str, List[str]]:
        """
        Given the name of a data, and a filter function, find the section and subsections for that data. 
        The filter function can be used to get particular only particular sections and its subsections.
        :param dataName: The name of the data to set section and subsections for
        :param filter: A function to filter out sections and get only the section of interest
        :return: A dictionary of section name to a list of the name of the subsection it has.
        """  
        pass
    
    @abstractmethod
    def getAllAvailableData(self, regex : re.Pattern) -> List[str]:
        """
        Given a regex pattern, find all data name that match the regext pattern
        :param regex: Regex pattern used to match data name. Pre-build regex pattern can be found in the constants file of the DataManager folder.
        :return: return a list of available data names.
        """  
        pass
        

    @abstractmethod 
    def findAllYearAngosticDataName(self)->List[str]:
        """
        Find all name of year agnostic data/
        :return: return a list of available year agnostic data names.
        """  
        pass 

    @abstractmethod
    def getAllAvailableYearsSorted(self) -> List[Tuple[str,str]]:
        """
        Get all available years with data that can be queried on.
        :return: A list of tuple. Each tuple contains two string: start year and end year.
        """  
        pass

    @abstractmethod
    def getAvailableDataForSpecificYearRange(self, startYear : str, endYear : str) -> List[str]:
        """
        Given start year and end year return a list of data names for available for that start year and end year
        :return: A list of string containing data names available.
        """  
        pass


    @abstractmethod
    def getSections(self, dataName) -> List[str]:
        """
        Given a data name, get a list of sections for that.
        :return: A list of section name for the data name.
        """  
        pass




    async def determineMatrixToSearch(self, intent, entities, startYear : str, endYear : str) -> SparseMatrix:
        """
        Given intent and entities, this function will determine the specific sparse matrix to be searched by the knowledgebase's search algorithm
        
        intent: intent of the user interpreted by rasa
        entities: list entities extracted by rasa. Each element in the list is a python dictionary. For example:
        {'entity': 'year', 'start': 58, 'end': 62, 'confidence_entity': 0.997698962688446, 'role': 'to', 'confidence_role': 0.7497242093086243, 'value': '2022', 'extractor': 'DIETClassifier'}

        """ 
        section = intent.replace("_", " ")
        # if startYear == None or endYear == None:
        #     raise NoDataFoundException(NO_DATA_EXIST_MESSAGE, ExceptionTypes.NoDataFoundAtAll)
        

        isYearAgnostic = False
        yearAgnosticDataName = self.findAllYearAngosticDataName()
        for dataName in yearAgnosticDataName:
            sections = self.getSections(dataName)
            if intent in sections:
                isYearAgnostic = True
                break


        startYear = str(startYear)
        endYear = str(endYear)
        exceptionToThrow = NoDataFoundException(NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=startYear, end=endYear), ExceptionTypes.NoDataFoundForAcademicYearException)
        
        sparseMatrices = []
        if isYearAgnostic:
            sparseMatrices = await self.getDataBySection(section, exceptionToThrow)
        else:
            sparseMatrices = await self.getDataBySection(section, exceptionToThrow, startYear, endYear)
            
        errorMessage = NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = section, start= str(startYear), end = str(endYear))
        selectedSparseMatrix = self.determineBestMatchingMatrix(sparseMatrices, entities, errorMessage)     
        return selectedSparseMatrix
       



    def determineBestMatchingMatrix(self, topicData : TopicData, entities : Dict, errorMessage : str) ->  List[SparseMatrix]:
        """
        This function will determine which sparse matrix under an intent should we search based on the given entities.

        First, it will check if any of the entity labels includes any subsections sparse matrix for the topic
        corresponding to the detected intent. For example, if an entity with race label was detected with enrollment intent, 
        it will tell TopicData for enrollemnt if it has a sparse matrix of the name "race"
        If there is one it will return it. Otherwise it will do the following:

        For each sparse matrix, it will calculate the number of entities that the sparse matrix has corresponding columns for.
        Then this function will find and return sparse matrix with the highest match number.
        We do this because for example, for enrollment, there are two matrix, one for general enrollment info and one for enrollment by race
        and if the user asks something like "how many hispanics male student are enrolled?" Should we use the general matrix that has gender
        or should we use the enrollment by race that has information on hispanic student enrollment?  

        If enrollment by race matrix has information about hispanic male enrollment, this algorithm would choose that. But in this case,
        there is no such information. so we can use any matrix. 

        However, if the user specify something like degree-seeking which is a column on both race and general enrollment matrix,
        we would want to use the genereal enrollment matrix but there will be a tie. So in this case, we use the first matrix for tie,
        which will be general enrollment.

        """
        doesEntityMapToAnySubsections, sparseMatricesFound = topicData.doesEntityIncludeAnySubsections(entities)
        candidates = list(topicData.getSparseMatrices().values())
      
        if doesEntityMapToAnySubsections:
            candidates = sparseMatricesFound
            
        maxMatch = []
        currMax = 0
        entityValues = []
        for entity in entities:
            entityValues.append(entity["value"])

        entityValues = list(set(entityValues))
        for sparseMatrix in candidates:  
            # print(sparseMatrix.sparseMatrixDf)
            # print(sparseMatrix.subSectionName)              
            entitiesMatchCount : int  = sparseMatrix.determineEntityMatchToColumnCount(entityValues)
            if entitiesMatchCount>currMax:
                maxMatch = []
                maxMatch.append(sparseMatrix)
                currMax = entitiesMatchCount
            elif entitiesMatchCount == currMax:
                maxMatch.append(sparseMatrix)

        if len(maxMatch) == 0:
            raise NoDataFoundException(errorMessage, ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)

        return maxMatch



 