

from abc import ABC, abstractmethod
from typing import Dict, List

from Parser.QuestionAnswer import QuestionAnswer
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from actions.entititesHelper import removeLowConfidenceEntities

class DataParser(ABC):

    def __init__(self):
        self.numberEntityExtractor = NumberEntityExtractor()
        self.entityConfidenceKey = "confidence_entity"
        self.confidenceThreshold = 0.5
    
    @abstractmethod
    def parse(self, subsectionName : str , questionAnswers : List[QuestionAnswer]):
        pass

    
    