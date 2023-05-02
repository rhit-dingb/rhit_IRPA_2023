
from abc import ABC, abstractmethod
from typing import List
import pandas as pd
from Parser.QuestionAnswer import QuestionAnswer
class DataLoader(ABC):
    """
    Abstract class responsible for processing and reading the input data of different forms.
    """
    def __init__(self):
        self.sectionFullNameToQuestionAnswers = dict()
        self.METADATA_KEY = "metadata"

    @abstractmethod
    def loadData(self, data): 
        """
        Given the input data represented in some way, read it and populate the sectionFullNameToQuestionAnswer dictionary.
        """
        pass

   
    def getAllSectionDataFullName(self) -> List[str] :
        return self.sectionFullNameToQuestionAnswers.keys()
    
    
    def getQuestionsAnswerForSection(self, sectionName) -> QuestionAnswer :
       if sectionName in self.sectionFullNameToQuestionAnswers.keys():
           return self.sectionFullNameToQuestionAnswers[sectionName]
       else:
           return []

    def convertDataframeToQuestionAnswer(self, questionAnswersDataFrame : pd.DataFrame, sheetName : str) -> List[QuestionAnswer]:
        """
        Given a pandas data frame containing question and answers, and metadata. Convert to a list of QuestionAnswer data model.
        The data frame looks exactly like a sheet on the input excel data.

        :param questionAnswersDataFrame: Pandas dataframe representing a sheet on the input excel file
        :param sheetName: The name of the sheet.
        """
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