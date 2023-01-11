from typing import List
from Parser.CDSDataLoader import CDSDataLoader
from rhit_IRPA_2023.Parser.QuestionAnswer import QuestionAnswer


class JsonCDSDataLoader(CDSDataLoader):
    def __init__(self):
        super().__init__()

    def loadData(self, inputExcelJsonData): 
        self.inputExcelJsonData = inputExcelJsonData


    #Get all section that "we need to parse into sparse matrix, including sub sections 

    def getAllSectionDataFullName(self) -> List[str] : 
        pass


    def getQuestionsAnswerForSection(self, sectionName) -> QuestionAnswer:
        pass
