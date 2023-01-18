
from typing import Dict, List
from Knowledgebase.SearchResultType import SearchResultType
from Knowledgebase.constants import PERCENTAGE_FORMAT
from Knowledgebase.constants import DOLLAR_FORMAT

class SearchResult():
    def __init__(self, answer, entitiesUsed : List[Dict[str, str]], type : SearchResultType, realQuestion : str):
        # print("CHANGE ANSWER")
        # print(answer)
        self.answer = str(answer)
        self.entitiesUsed = entitiesUsed
        self.type = type
        self.realQuestion = realQuestion
        self.entitiesForRealQuestion = []

    def setEntitiesForRealQuestion(self,entities):
        self.entitiesForRealQuestion = entities

    def changeAnswer(self,answer : str):
        if self.type == SearchResultType.PERCENTAGE:
           self.answer = PERCENTAGE_FORMAT.format(value = answer)
        elif self.type == SearchResultType.DOLLAR:  
            self.answer = DOLLAR_FORMAT.format(value= answer)
        else:
            self.answer = answer
            
    def addEntities(self, entities : Dict[str, str]):
        self.entitiesUsed = self.entitiesUsed + entities

