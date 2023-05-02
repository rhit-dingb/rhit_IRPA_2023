from typing import Dict, List
from Data_Ingestion.SparseMatrix import SparseMatrix
from abc import ABC, abstractmethod

class DataWriter(ABC):
    """
    Abstract class whose concrete implementation will take in the parsed data and write to a data source.
    """
    def __init__(self):
        pass

    @abstractmethod
    def write(self, parsedData) -> None:
        """
        Given the parsedData, write it to a data source. The specific type of the parsedData depends the specific implementation.
        """
        pass