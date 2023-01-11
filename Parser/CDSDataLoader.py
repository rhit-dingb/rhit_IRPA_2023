
from abc import ABC, abstractmethod
from typing import List

from Parser.QuestionAnswer import QuestionAnswer
class CDSDataLoader(ABC):
    def __init__(self):
        self.sectionFullNameToQuestionAnswers = dict()

    @abstractmethod
    def loadData(self): 
        pass

    #Get all section that "we need to parse into sparse matrix, including sub sections 
    def getAllSectionDataFullName(self) -> List[str] :
        return self.sectionFullNameToQuestionAnswers.keys()
    
    
    def getQuestionsAnswerForSection(self, sectionName) -> QuestionAnswer :
       if sectionName in self.sectionFullNameToQuestionAnswers.keys():
           return self.sectionFullNameToQuestionAnswers[sectionName]
       else:
           return []