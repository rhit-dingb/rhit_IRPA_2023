
from typing import Dict, List

from Data_Ingestion.SparseMatrix import SparseMatrix

from abc import ABC, abstractmethod
import pandas as pd

class ShouldAddRowStrategy(ABC):
    def __init__(self):
        super().__init__()
  
    @abstractmethod
    def determineShouldAddRow(self, row : pd.Series , entities : List[Dict], sparseMatrix : SparseMatrix) -> List[Dict]:
        """
        Abstract method to determine if a row(a particular answer) in the sparse matrix should be used as part of the output--
        whether that be adding to an existing sum, or appending to an existing of answers.
        :param row: Row in a Pandas dataframe, which is a pandas series. 
        :param entities: Entities extracted from user queries.
        :param sparseMatrix: The selected sparse matrix that is searched on.
        :return: A list of entities that was matched. If this row should be used, return an non empty list otherwise, return empty list
        """
        pass