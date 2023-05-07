
import asyncio
import json
from typing import Dict, List
import unittest
from unittest import mock
from unittest.mock import patch

from pymongo import MongoClient
from DataManager.constants import *
from Knowledgebase.SparseMatrixKnowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Parser.ExcelCDSDataLoader import ExcelCDSDataLoader
from Parser.MongoDbNoChangeDataWriter import MongoDbNoChangeDataWriter
from Parser.NoChangeDataParser import NoChangeDataParser
from Parser.ParserFacade import ParserFacade
from Parser.JsonDataLoader import JsonDataLoader
from Data_Ingestion.SubsectionQnA import SubsectionQnA
from Parser.QuestionAnswer import QuestionAnswer
from tests.testUtils import checkAnswersMatch, createEntityObjHelper, createFakeTracker, extractOutput
from Data_Ingestion.ConvertToSparseMatrixDecorator import ConvertToSparseMatrixDecorator
from Data_Ingestion.MongoProcessor import MongoProcessor
from DataManager.MongoDataManager import MongoDataManager
from tests.test_knowledgebase import TOTAL_UNDERGRADUATES
import json
from bson import json_util
from UnansweredQuestions.UnansweredQuestionAnswerEngine import UnansweredQuestionAnswerEngine
from UnansweredQuestions.MongoDBUnansweredQuestionConnector import MongoDBUnansweredQuestionConnector
from UnansweredQuestions.UnasweredQuestionDBConnector import UnansweredQuestionDbConnector


# class test_integration_knowledgebase_and_dataSource(unittest.TestCase):
#     def setUp(self):
        
#         #SET UP THE TEST DATABASE'
#         self.testDbName= "TEST_2020_2021"
#         self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
#         excelCDSDataLoader = ExcelCDSDataLoader("./tests/testMaterials/inputData/TEST_2020_2021.xlsx")
#         excelCDSDataLoader.loadData()
#         print(excelCDSDataLoader.getAllSectionDataFullName())
#         dataParser = NoChangeDataParser()
#         dataWriter = MongoDbNoChangeDataWriter(self.testDbName, client=self.client)
#         parserFacade = ParserFacade(dataLoader=excelCDSDataLoader, dataWriter=dataWriter, dataParser=dataParser)
#         asyncio.run(parserFacade.parse())


#         mongoProcessor = MongoProcessor()
#         mongoProcessor = ConvertToSparseMatrixDecorator(mongoProcessor)
#         self.dataManager = MongoDataManager(mongoProcessor)
#         self.knowledgeBase = SparseMatrixKnowledgeBase(
#            self.dataManager)
        
#         self.knowledgeBase.getAllEntityForRealQuestionFoundForAnswer = self.fakeGetAllEntityForRealQuestionFoundForAnswer
#         # self.extractOutput = extractOutput
#         # self.knowledgeBase.constructOutput = self.extractOutput

#     def tearDown(self) -> None:
#         self.dataManager.deleteData(self.testDbName)
#         self.client.close()
        

#     async def fakeGetAllEntityForRealQuestionFoundForAnswer(self, searchResults):
#         pass


    
#     def test_integration_ask_for_total_undergraduates_enrollment(self):
      

#         question = "how many undergraduate students are enrolled?"
#         answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
#             createEntityObjHelper("undergraduate"),
#         ],  2020, 2021, completeSentence=False))

#         answerStr = [answer.answer for answer in answers]
#         self.assertEqual(answerStr, [str(TOTAL_UNDERGRADUATES)])


# class test_integration_data_parser_and_dataSource(unittest.TestCase):
#     def setUp(self):
#         self.testDbName= "TEST_2020_2021"
#         mongoProcessor = MongoProcessor()
#         self.dataManager = MongoDataManager(mongoProcessor)
#         f = open('./tests/testMaterials/parserData/JsonInputExcelData.json')
#         self.data : Dict[str, any] = json.load(f)
#         f.close()

#         self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
#         self.jsonCdsLoader = JsonDataLoader()
#         self.jsonCdsLoader.loadData(self.data)
#         self.dataParser = NoChangeDataParser()
#         self.dataWriter = MongoDbNoChangeDataWriter(self.testDbName, client = self.client)
#         self.parserFacade = ParserFacade(dataLoader=self.jsonCdsLoader, dataWriter=self.dataWriter, dataParser=self.dataParser)

#         #Write to database
#         asyncio.run(self.parserFacade.parse())

#     def tearDown(self) -> None:
#         self.dataManager.deleteData(self.testDbName)
#         self.client.close()
        

    
#     def test_integration_data_written_to_datasource_should_have_correct_sections(self):
#         expectedSections = self.jsonCdsLoader.getSections()
#         writtenSections = self.dataManager.getSections(self.testDbName)
#         print(expectedSections)
#         print(writtenSections)
#         self.assertCountEqual(expectedSections, writtenSections)

#     def test_integration_data_written_to_datasource_should_have_correct_data(self):
#         sectionToSubsections = self.dataManager.getSectionAndSubsectionsForData(self.testDbName)
    
#         def useTestDb(db):
#             return db == self.testDbName
        
#         for section in sectionToSubsections:
#             subsectionQnAs : List[SubsectionQnA] = asyncio.run(self.dataManager.getDataBySection(section.lower(), Exception(), "2020", "2021", databaseFilter = useTestDb))
#             for subsectionQnA in subsectionQnAs:
#                 sectionFullName = section + subsectionQnA.subSectionName
#                 actualQuestionAnswers : List[QuestionAnswer]= self.jsonCdsLoader.getQuestionsAnswerForSectionAndSubsection(sectionFullName)
#                 for questionAnswer in actualQuestionAnswers:
#                     self.assertIn(questionAnswer.getQuestion(), subsectionQnA.getQuestions())
#                     self.assertIn(questionAnswer.getAnswer(), subsectionQnA.getAnswers())
#             # self.assertEqual(data)



class test_integration_unansweredQuestionUnit_and_dataSource(unittest.TestCase):
    def setUp(self):
       self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
       self.testDbName = "TestUnansweredQuestion"
       self.unansweredQuestionDbConnection = self.client[self.testDbName]
       self.unansweredQuestionDataSource = MongoDBUnansweredQuestionConnector(self.unansweredQuestionDbConnection)
       self.unansweredQuestionEngine = UnansweredQuestionAnswerEngine(self.unansweredQuestionDataSource)
       self.writeFakeData()
    
    def writeFakeData(self):
        f = open('./tests/testMaterials/unansweredQuestionData/questionAnswers.json')
        self.data : Dict[str, any] = json.load(f)
        self.data = self.data["data"]

        f.close()

        for questionAnswer in self.data:
            question = questionAnswer["question"]
            answer = questionAnswer["answer"]
            id = self.unansweredQuestionDataSource.addNewUnansweredQuestion(question=question, chatbotAnswers=[])
            self.unansweredQuestionDataSource.provideAnswerToUnansweredQuestion(id, answer = answer)


    def tearDown(self) -> None:
        # self.client.drop_database(self.testDbName)
        self.client.close()    

    def test_integration_ask_question_with_low_confidence_should_return_no_answer(self):
        # unansweredQuestionDbConnector : UnansweredQuestionDbConnector = MongoDBUnansweredQuestionConnector()
        # print(unansweredQuestionDbConnector.getAllUnansweredQuestionAndAnswer())
        questionToAsk = "What is the largest animal in the world?"
        answers = self.unansweredQuestionEngine.answerQuestion(questionToAsk)
        self.assertEqual([],answers)
    
    def test_integration_ask_question_with_high_confidence_should_return_answer(self):
        # unansweredQuestionDbConnector : UnansweredQuestionDbConnector = MongoDBUnansweredQuestionConnector()
        # print(unansweredQuestionDbConnector.getAllUnansweredQuestionAndAnswer())
        questionToAsk = "What planet hottest in solar system?"
        answers = self.unansweredQuestionEngine.answerQuestion(questionToAsk)
        self.assertEqual(["Venus"],answers)
    
    



if __name__ == '__main__':
    unittest.main()
