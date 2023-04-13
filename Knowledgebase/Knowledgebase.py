# This is be a interface that will be implemented by concrete classes.
from copy import deepcopy
from typing import List
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from abc import ABC, abstractmethod

from Data_Ingestion.SparseMatrix import SparseMatrix
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel


class KnowledgeBase(ABC) :
    def __init__(self):
        pass
    
    @abstractmethod
    def getAvailableOptions(self, intent, entities, startYear, endYear):
        pass
    
    @abstractmethod
    def searchForAnswer(self, question, intent, entitiesExtracted, startYear, endYear) -> List[ChatbotAnswer]:
        pass 

    # this function will aggregate number given a range, using the generator to create column name for those rows and 
    # sum up the value for those rows
    @abstractmethod
    def aggregateDiscreteRange(self, entities, dataModel, isSumming):
        pass

    @abstractmethod
    def calculatePercentages(self, searchResults, entitiesForEachResult, dataModel):
        pass


    @abstractmethod
    def train(self, trainingLabels : List[MultiFeedbackLabel])-> bool:
        pass
    
    @abstractmethod
    async def dataUploaded(self, dataName):
        pass

    @abstractmethod
    def dataDeleted(self, dataName ):
        pass
    
