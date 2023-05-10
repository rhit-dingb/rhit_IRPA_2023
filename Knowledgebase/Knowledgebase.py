
from typing import Dict, List, Tuple
from Knowledgebase.SparseMatrixKnowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy

from abc import ABC, abstractmethod

from Data_Ingestion.SparseMatrix import SparseMatrix
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel


class KnowledgeBase(ABC) :
    def __init__(self):
        pass
    
    
    @abstractmethod
    def searchForAnswer(self, question : str, intent : str, entitiesExtracted : List[Dict[str, str]], startYear : str, endYear : str) -> Tuple[List[ChatbotAnswer], bool]:
        """
        An abstract method that concrete knowledgebase class need to implement to search for answers.
        :param question:question that the user asked
        :param intent: The intent detected by Rasa based on the user query
        :entitiesExtracted: entities extracted, looking something like:
        [
            {
            "start": 18,
            "end": 21,
            "value": 2,
            "entity": "guests",
            "confidence": 0.6886989589,
            "extractor": "CRFEntityExtractor",
            }
        ]

        :param startYear: start year to query the data
        :param endYear: end year to query the data
        :return: A tuple, the first element is the list of ChatbotAnswers, the second element is whether or not the next knowledgebase should search for answer.
        """
        pass 


    @abstractmethod
    def train(self, trainingLabels : List[MultiFeedbackLabel], callback)-> bool:
        """
        An abstract method implemented by the concrete knowledgebase class to finetune itself given a list of MultiFeedbackLabel and a callback function. 
        :param trainingLabels: List of MultiFeedbackLabel. Each MultiFeedback label corresponds to a query made by the user and has a list of FeedbackLabel object. Each FeedbackLabel corresponds to an answer 
        provided by the chatbot.

        :param callback: A callback function, taking in a boolean as parameter that should be invoked when training is done. The boolean parameter 
        tells the function if the training is successful or not.

        :return: return boolean whether training was successful or not.
        """
        pass
    
    @abstractmethod
    async def dataUploaded(self, dataName : str, startYear : str = None, endYear : str = None ):
        """
        Concrete implementation of the knowledgebase can implement this function to react to when data is uploaded.
        Note that this function is async, so the "await" keyword need to be used when calling it.
        :param dataName: Name of the data that is uploaded.
        :param startYear: Optional parameter specifying the start year of the data being uploaded. When start year and end year is none, the data is a
        year agnostic data.
        :param endYear: Optional parameter specifying the end year of the data being uploaded.
        :return: none
        """
        pass

    @abstractmethod
    def dataDeleted(self, dataName : str ):
        """
        Concrete implementation of the knowledgebase can implement this function to react to when data is deleted.
        :param dataName: The name of the data that has been deleted.
        :return: none
        """
        pass
    
