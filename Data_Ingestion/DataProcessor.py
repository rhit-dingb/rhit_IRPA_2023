
from abc import ABC, abstractmethod
class DataProcessor(ABC):
    """
    Abstract class for concrete class repsonsible for processing data from a data source to a internal data model.
    """
    @abstractmethod
    def getDataByDbNameAndSection(self, client, section : str, dbName : str):
        pass
    
