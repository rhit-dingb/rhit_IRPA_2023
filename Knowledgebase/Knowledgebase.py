# This is be a interface that will be implemented by concrete classes.
from copy import deepcopy
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from abc import ABC, abstractmethod

from Data_Ingestion.SparseMatrix import SparseMatrix
class KnowledgeBase(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def getAvailableOptions(self, key):
        pass
    
    @abstractmethod
    def searchForAnswer(self, intent, entities):
        pass 

    # this function will aggregate number given a range, using the generator to create column name for those rows and 
    # sum up the value for those rows
    @abstractmethod
    def aggregateDiscreteRange(self, entities, sparseMatrix : SparseMatrix, isSumming):
        pass

    @abstractmethod
    def calculatePercentages(self, searchResults, entitiesForEachResult, sparseMatrix : SparseMatrix):
        pass
