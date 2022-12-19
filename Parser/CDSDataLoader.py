

from typing import List, Dict
from Parser.QuestionAnswer import QuestionAnswer
import pandas as pd

class CDSDataLoader():
    def __init__(self, path, ):
        self.data = dict()
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
                    print("SET TO TRUEs")
                    #If metadata marker found, skip the metadata marker and mark the thing below as metadata.
                    continue
               
                questionAnswerObj = QuestionAnswer(questionAnswerRow["Question"], questionAnswerRow["Answer"], [], isMetaData=isMetaData)
                questionsAnswers.append(questionAnswerObj)
               
                print(questionAnswerObj.question)

            lowerSheetName = sheetName.lower()
            self.data[lowerSheetName] = questionsAnswers
        
    
    #Get all section that "we need to parse into sparse matrix, including sub sections 
    def getAllSections(self) -> List[str] :
        return self.data.keys()
    
    
    def getQuestionsAnswerForSection(self, sectionName) -> QuestionAnswer :
       if sectionName in self.data.keys():
           return self.data[sectionName]
       else:
           return []