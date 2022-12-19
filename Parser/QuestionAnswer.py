#Internal data model representing a question supported by chatbot and answer provided by client
from typing import List
class QuestionAnswer():
    def __init__(self, question, answer, entities, isMetaData):
       self.question : str = question
       self.answer : str = answer
       self.entities : List[str] = entities
       self.isMetaData = isMetaData
       
    
    def setEntities(self, entities : List[str]):
        self.entities = entities
    
    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer