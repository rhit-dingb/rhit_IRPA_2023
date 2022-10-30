from Data_Ingestion.SparseMatrix import SparseMatrix

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

    def getSparseMatrices(self) -> dict[str, SparseMatrix]:
        return self.sparseMatrices

    def hasData(self) -> bool : 
        return not len(self.sparseMatrices.keys()) == 0


    def doesEntityIncludeAnySubsections(self, entities) ->  tuple[bool, SparseMatrix]:
        for entity in entities:
            label : str = entity["entity"]
            if label in self.sparseMatrices:
                return (True, self.sparseMatrices[label])
                
        return (False, None)
