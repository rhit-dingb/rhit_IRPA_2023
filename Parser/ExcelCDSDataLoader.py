

from typing import List, Dict
from Parser.QuestionAnswer import QuestionAnswer
from Parser.CDSDataLoader import CDSDataLoader
import pandas as pd

class ExcelCDSDataLoader(CDSDataLoader):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.excelConnector = pd.ExcelFile(path)
        self.METADATA_KEY = "metadata"
    
    def loadData(self): 
       for sheetName in self.excelConnector.sheet_names:
            #questionAnswersDataFrame = self.excelConnector.parse(sheetName)
            questionAnswersDataFrame = pd.read_excel(self.path, sheet_name=sheetName, dtype={'Answer': object} )
            questionAnswersDataFrame  =  questionAnswersDataFrame.astype(str)
           
            # questionAnswersDataFrame["Answer"] = questionAnswersDataFrame["Answer"].astype("string")
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
               
                print(questionAnswerObj.question)

            lowerSheetName = sheetName.lower()
            self.sectionFullNameToQuestionAnswers[lowerSheetName] = questionsAnswers
        
    
