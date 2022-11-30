from typing import List
from Data_Ingestion.SparseMatrix import SparseMatrix

class SparseMatrixDataWriter():
    def __init__(self):
        raise Exception("This is an abstract class please inherit and override with an concrete subclass")
     
       
    def writeSparseMatrix(self, sparseMatrix : SparseMatrix) -> None:
         raise Exception("This is an abstract class please inherit and override with an concrete subclass")