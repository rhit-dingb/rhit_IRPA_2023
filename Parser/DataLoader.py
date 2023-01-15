
from abc import ABC, abstractmethod
from typing import List

from Parser.QuestionAnswer import QuestionAnswer
class DataLoader(ABC):
    def __init__(self):
        self.sectionFullNameToQuestionAnswers = dict()
        self.METADATA_KEY = "metadata"

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

    def convertDataframeToQuestionAnswer(self, questionAnswersDataFrame, sheetName):
        questionsAnswers = []
        isMetaData = False
        for i in range(questionAnswersDataFrame.shape[0]):
            questionAnswerRow = questionAnswersDataFrame.loc[i]
            
            if questionAnswerRow["Question"].replace(" ", "").lower() == self.METADATA_KEY:
                isMetaData = True
                #If metadata marker found, skip the metadata marker and mark the thing below as metadata.
                continue
            
            questionAnswerObj = QuestionAnswer(questionAnswerRow["Question"], questionAnswerRow["Answer"], [], isMetaData=isMetaData)
            questionsAnswers.append(questionAnswerObj)
            
            # print(questionAnswerObj.question)

        lowerSheetName = sheetName.lower()
        self.sectionFullNameToQuestionAnswers[lowerSheetName] = questionsAnswers