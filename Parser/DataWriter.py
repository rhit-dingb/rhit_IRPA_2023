from typing import Dict, List
from Data_Ingestion.SparseMatrix import SparseMatrix
from abc import ABC, abstractmethod

class DataWriter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def write(self, parsedData) -> None:
        pass