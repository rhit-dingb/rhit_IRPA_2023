

from abc import ABC, abstractmethod
from typing import Dict, List

from Parser.QuestionAnswer import QuestionAnswer
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from actions.entititesHelper import removeLowConfidenceEntities

class DataParser(ABC):
    """
    Abstract class whose concrete implementation is responsible for parsing a list of QuestionAnswer object into a specific form of data 
    that can be written to a data source.
    """
    def __init__(self):
        self.numberEntityExtractor = NumberEntityExtractor()
        self.entityConfidenceKey = "confidence_entity"
        self.confidenceThreshold = 0.5
    
    @abstractmethod
    def parse(self, subsectionName : str , questionAnswers : List[QuestionAnswer]):
        """
        This function takes in a list of QuestionAnswer object and convert it to a different form of data(depending on the concrete implementation)
        that can be written to a data source

        :param subsectionName: Name of the subsection that can be parsed
        :param questionAnswers: List of QuestionAnswer corresponding to the given subsection.
        :return: The return type depend on the specific implementation. 
        """
        pass

    
    