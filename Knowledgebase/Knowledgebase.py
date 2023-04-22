# This is be a interface that will be implemented by concrete classes.
from copy import deepcopy
from typing import List, Tuple
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from abc import ABC, abstractmethod

from Data_Ingestion.SparseMatrix import SparseMatrix
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel


class KnowledgeBase(ABC) :
    def __init__(self):
        pass
    
    
    @abstractmethod
    def searchForAnswer(self, question, intent, entitiesExtracted, startYear, endYear) -> Tuple[List[ChatbotAnswer], bool]:
        pass 


    @abstractmethod
    def train(self, trainingLabels : List[MultiFeedbackLabel], callback)-> bool:
        pass
    
    @abstractmethod
    async def dataUploaded(self, dataName : str, startYear : str = None, endYear : str = None ):
        pass

    @abstractmethod
    def dataDeleted(self, dataName : str ):
        pass
    
