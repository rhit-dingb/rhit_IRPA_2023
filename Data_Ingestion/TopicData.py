from Data_Ingestion.SparseMatrix import SparseMatrix
from typing import Dict, Tuple

"""
Internal data model representing a topic in the CDS data. A topic can have many sparse matrices, each sparse matrix represents
a subsection. For example: the topic of enrollment has both general enrollment and enrollment by race.
"""
class TopicData():
    def __init__(self, topic : str):
        self.name : str = topic
        self.sparseMatrices : dict[str, SparseMatrix] = dict()


    def addSparseMatrix(self, key: str, sparseMatrix : SparseMatrix):
        self.sparseMatrices[key] = sparseMatrix

    def getSparseMatrices(self) -> Dict[str, SparseMatrix]:
        return self.sparseMatrices

    def hasData(self) -> bool : 
        return not len(self.sparseMatrices.keys()) == 0


    def doesEntityIncludeAnySubsections(self, entities) ->  Tuple[bool, SparseMatrix]:
        subSectionSparseMatrices = []
        for entity in entities:

            label : str = entity["entity"]
            for key in self.sparseMatrices.keys():
                keywords = key.split(" ")
                if label in keywords:
                    subSectionSparseMatrices.append(self.sparseMatrices[key])

        if len(subSectionSparseMatrices) == 0:
            return (False, None)
        else:
            return (True, subSectionSparseMatrices )
                
        
