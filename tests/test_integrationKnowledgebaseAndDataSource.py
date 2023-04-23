
import asyncio
import unittest
from unittest import mock
from unittest.mock import patch

from pymongo import MongoClient
from DataManager.constants import *
from Knowledgebase.Knowledgebase import KnowledgeBase
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from OutputController import output
from Parser.ExcelCDSDataLoader import ExcelCDSDataLoader
from Parser.MongoDbNoChangeDataWriter import MongoDbNoChangeDataWriter
from Parser.NoChangeDataParser import NoChangeDataParser
from Parser.ParserFacade import ParserFacade
from tests.testUtils import checkAnswersMatch, createEntityObjHelper, createFakeTracker, extractOutput
from Data_Ingestion.ConvertToSparseMatrixDecorator import ConvertToSparseMatrixDecorator
from Data_Ingestion.MongoProcessor import MongoProcessor
from DataManager.MongoDataManager import MongoDataManager
from tests.test_knowledgebase import TOTAL_UNDERGRADUATES


class test_integration_knowledgebase_and_dataSource(unittest.TestCase):
    def setUp(self):
        
        #SET UP THE TEST DATABASE'
        self.testDbName= "TEST_2020_2021"
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        excelCDSDataLoader = ExcelCDSDataLoader("./tests/testMaterials/inputData/TEST_2020_2021.xlsx")
        dataParser = NoChangeDataParser()
        dataWriter = MongoDbNoChangeDataWriter(self.testDbName, client=self.client)
        parserFacade = ParserFacade(dataLoader=excelCDSDataLoader, dataWriter=dataWriter, dataParser=dataParser)
        asyncio.run(parserFacade.parse())


        mongoProcessor = MongoProcessor()
        mongoProcessor = ConvertToSparseMatrixDecorator(mongoProcessor)
        self.dataManager = MongoDataManager(mongoProcessor)
        self.knowledgeBase = SparseMatrixKnowledgeBase(
           self.dataManager)
        
        self.knowledgeBase.getAllEntityForRealQuestionFoundForAnswer = self.fakeGetAllEntityForRealQuestionFoundForAnswer
        # self.extractOutput = extractOutput
        # self.knowledgeBase.constructOutput = self.extractOutput

    def tearDown(self) -> None:
        self.dataManager.deleteData(self.testDbName)

    async def fakeGetAllEntityForRealQuestionFoundForAnswer(self, searchResults):
        pass


    
    def test_integration_ask_for_total_undergraduates_enrollment(self):
        dataParser = NoChangeDataParser()
        excelCDSDataLoader = ExcelCDSDataLoader("./tests/testMaterials/inputData/TEST_2020_2021.xlsx")
        dataWriter = MongoDbNoChangeDataWriter(self.testDbName, client=self.client)
        parserFacade = ParserFacade(dataLoader=excelCDSDataLoader, dataWriter=dataWriter, dataParser=dataParser)
        asyncio.run(parserFacade.parse())

        question = "how many undergraduate students are enrolled?"
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
            createEntityObjHelper("undergraduate"),
        ],  2020, 2021, completeSentence=False))

        answerStr = [answer.answer for answer in answers]
        self.assertEqual(answerStr, [str(TOTAL_UNDERGRADUATES)])

    

if __name__ == '__main__':
    unittest.main()
