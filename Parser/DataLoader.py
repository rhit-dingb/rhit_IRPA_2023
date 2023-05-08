
from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd
from Parser.QuestionAnswer import QuestionAnswer
class DataLoader(ABC):
    """
    Abstract class responsible for processing and reading the input data of different forms.
    """
    def __init__(self):
        self.METADATA_KEY = "metadata"
        self.seperator = "_"
        self.sectionFullNameToQuestionAnswers : Dict[str, List[QuestionAnswer]] = dict()

    @abstractmethod
    def loadData(self, data): 
        """
        Given the input data represented in some way, read it and populate the sectionFullNameToQuestionQuestionAnswer 
        """
        pass

    
    # @abstractmethod
    # def getSectionToSubsection() -> Dict[Dict[str]]:
    #     """

    #     """
    #     pass

    def getSections(self):
        sections = []
        for sectionToSubsectionFullName in self.sectionFullNameToQuestionAnswers.keys():
            sectionToSubsection = sectionToSubsectionFullName.split(self.seperator)
            if sectionToSubsection[0] in sections:
                continue
            sections.append(sectionToSubsection[0])
        
        return sections
   
    def getAllSectionDataFullName(self) -> List[str] :
        return self.sectionFullNameToQuestionAnswers.keys()
    
    
    def getQuestionsAnswerForSectionAndSubsection(self, sectionToSubsectionFullName : str) -> QuestionAnswer :
       sectionToSubsectionFullName = sectionToSubsectionFullName.lower()
       if sectionToSubsectionFullName in self.sectionFullNameToQuestionAnswers.keys():
           return self.sectionFullNameToQuestionAnswers[sectionToSubsectionFullName ]
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

        return questionsAnswers