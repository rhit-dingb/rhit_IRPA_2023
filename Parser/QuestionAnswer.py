#Internal data model representing a question supported by chatbot and answer provided by client
from typing import List
class QuestionAnswer():
    def __init__(self, question : str, answer : str, entities, isMetaData):
       self.question : str = str(question).lower()
       self.answer : str = str(answer)
       self.entities : List[str] = entities
       self.isMetaData = isMetaData
       
    
    def setEntities(self, entities : List[str]):
        entitiesLowerCased = []
        for entity in entities:
            entitiesLowerCased.append(entity.lower())

        self.entities = entitiesLowerCased
    
    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer