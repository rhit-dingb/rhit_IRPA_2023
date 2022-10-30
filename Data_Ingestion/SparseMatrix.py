
"""
Internal data model representing a sparse matrix
"""

import pandas as pd
class SparseMatrix():
    def __init__(self, subSectionName, sparseMatrixDf):
        self.subSectionName = subSectionName
        self.sparseMatrixDf = sparseMatrixDf


    def getSparseMatrixDf(self):
        return self.sparseMatrixDf
    
    """
    This function determine the number of entities extracted that matches the columns of the sparse matrix
    """
    def determineEntityMatchToColumnCount(self, entities) -> int:
        entitiesMatchCount = 0
        for entity in entities:
            if entity["value"] in self.sparseMatrixDf.columns:
                entitiesMatchCount = entitiesMatchCount+1
                
        return entitiesMatchCount
        
