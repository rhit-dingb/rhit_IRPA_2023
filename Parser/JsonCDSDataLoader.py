from typing import Dict, List
from Parser.CDSDataLoader import CDSDataLoader
from Parser.QuestionAnswer import QuestionAnswer
import pandas as pd

# The input json payload will look something like this

# {
# 'data':
# {'General Info': 
    # [
    # {'Question': "What is Rose-Hulman's mailing address?", 'Answer': "Rose-Hulman's mailing address is 5500 Wabash Ave, Terre 
    # Haute, IN 47803", 'Complete Sentence?': 'Yes'}, 
    # {'Question': 'What is Rose-Hulman main phone number?', 'Answer': "Rose-Hulman's main phone number is (812) 877-1511", 'Complete Sentence?': 'Yes'}, 
    # {'Question': 'What is Rose-Hulman’s www home page address / website?', 'Answer': "Rose-Hulman's website is www.rose-hulman.edu", 'Complete Sentence?': 'Yes'}, 
    # .....],
   #'Enrollment_General': [.....], 
#  }
# }

class JsonCDSDataLoader(CDSDataLoader):
    def __init__(self):
        super().__init__()

    def loadData(self, inputExcelJsonData : Dict[str, List]): 
        for sectionAndSubsectionFullName in inputExcelJsonData.keys():
            sheetData = inputExcelJsonData[sectionAndSubsectionFullName]
            questionAnswersDataFrame = pd.DataFrame.from_dict(sheetData)
            self.convertDataframeToQuestionAnswer(questionAnswersDataFrame, sectionAndSubsectionFullName)
