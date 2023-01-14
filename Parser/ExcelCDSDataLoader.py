

from typing import List, Dict
from Parser.QuestionAnswer import QuestionAnswer
from Parser.CDSDataLoader import CDSDataLoader
import pandas as pd

class ExcelCDSDataLoader(CDSDataLoader):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.excelConnector = pd.ExcelFile(path)
      
    
    def loadData(self): 
       for sheetName in self.excelConnector.sheet_names:
            #questionAnswersDataFrame = self.excelConnector.parse(sheetName)
            questionAnswersDataFrame = pd.read_excel(self.path, sheet_name=sheetName, dtype={'Answer': object} )
            questionAnswersDataFrame  =  questionAnswersDataFrame.astype(str)
           
            # questionAnswersDataFrame["Answer"] = questionAnswersDataFrame["Answer"].astype("string")
            self.convertDataframeToQuestionAnswer(questionAnswersDataFrame)
        
    
