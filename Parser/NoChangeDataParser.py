


from typing import Dict, List, Tuple
from Parser.DataParser import DataParser

from Parser.QuestionAnswer import QuestionAnswer
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor

class NoChangeDataParser(DataParser):

    def __init__(self):
        pass
    
 
    def parse(self, subsectionName : str , questionAnswers : List[QuestionAnswer]) -> Tuple[str,  List[QuestionAnswer]]:
        return (subsectionName, questionAnswers)

    
    