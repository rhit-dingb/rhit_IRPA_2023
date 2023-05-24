
from typing import Dict, List, Tuple
from Exceptions.ExceptionTypes import ExceptionTypes



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

