from typing import List
from Data_Ingestion.SparseMatrix import SparseMatrix
from abc import ABC, abstractmethod

class SparseMatrixDataWriter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def writeSparseMatrices(self, sparseMatrices : List[SparseMatrix], sectionName : str) -> None:
        pass