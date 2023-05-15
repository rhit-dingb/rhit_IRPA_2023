

import asyncio
from copy import deepcopy
import json
from typing import Dict, List
import unittest
import os
import sys
from DataManager.MongoDataManager import MongoDataManager
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.ConvertToDocumentDecorator import ConvertToDocumentDecorator
import Data_Ingestion.constants as metadataConstants
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer

import tests.testUtils as testUtils
from Knowledgebase.DataModels.SearchResult import SearchResult


from Knowledgebase.SparseMatrixKnowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.QuestionAnswerKnowledgebase.QuestionAnswerKnowledgebase import QuestionAnswerKnowledgeBase
from Knowledgebase.SparseMatrixKnowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT
from unittest.mock import patch
from unittest import mock
from tests.testUtils import createEntityObjHelper
from unittest.mock import MagicMock

# These values are data from the 2020-2021 CDS dataset.
TOTAL_UNDERGRADUATES = 1972
TOTAL_UNDERGRADUATE_PART_TIME = 20
DEGREE_SEEKING_FIRST_TIME_FRESHMAN = 531
HISPANIC_STUDENTS_ENROLLMENT = 104
NON_FRESHMAN = 1427
DEGREE_SEEKING_FIRST_TIME_NON_FRESHMAN = 1082
TOTAL_GRADUATES = 18
DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED = 127
UNDERGRADUATE_DEGREE_SEEKING_HISPANIC_STUDENTS_ENROLLED = 104
UNDERGRADUATE_FIRST_TIME_DEGREE_SEEKING_UNKNOWN_RACE_STUDENT_ENROLLED = 6
UNDERGRADUATE_DEGREE_SEEKING_AFRICAN_AMERICAN_STUDEN_ENROLLED = 93
NON_FIRST_TIME = 0
NON_DEGREE_SEEKING_STUDENTS  = 3
TOTAL_UNDERGRADUATE_MALE = 1478

class SparseMatrix_knowledgebase_test(unittest.TestCase):
    def setUp(self):
        # self.knowledgeBase = SparseMatrixKnowledgeBase("../Data_Ingestion/CDS_SPARSE_ENR.xlsx")
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials/cdsTestData"))
       
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
        self.knowledgeBase.getAllEntityForRealQuestionFoundForAnswer = self.fakeGetAllEntityForRealQuestionFoundForAnswer
        self.extractOutput = testUtils.extractOutput
        self.knowledgeBase.constructOutput = self.extractOutput

    async def fakeGetAllEntityForRealQuestionFoundForAnswer(self, searchResults : List[SearchResult]):
        pass

    
    # def test_give_no_entities_should_sum_up_everything(self):
    #     answers = asyncio.run(self.knowledgeBase.searchForAnswer("enrollment", [
    #     ], self.defaultShouldAddRowStrategy, self.extractOutput)
    #     self.assertEqual(answers, [str(TOTAL_UNDERGRADUATES+TOTAL_GRADUATES, 2020, 2021)])

    
    def test_when_ask_for_total_graduates_enrollment_should_return_correct_value(self):
        question = "How many graduate students are enrolled?"
        # question, intent, entitiesExtracted, startYear, endYear, 

        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
            createEntityObjHelper("graduate"),
        ], 2020, 2021))
        
        self.assertEqual(answers, [str(TOTAL_GRADUATES)])


    def test_when_ask_for_non_degree_seeking_should_return_correct_value(self):
        question = "How many non-degree-seeking students are there?"
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
            createEntityObjHelper("non-degree-seeking"),
        ], 2020, 2021))

        self.assertEqual(answers, [str(NON_DEGREE_SEEKING_STUDENTS)])

    def test_ask_for_full_time_undergraduate_men_non_freshmans(self):
        question = "How many undergraduate men are non-freshman?"
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
            createEntityObjHelper("full-time"),
            createEntityObjHelper("degree-seeking"),
            createEntityObjHelper("male"),
            createEntityObjHelper("non-freshman"),
            ],  2020, 2021))
        
        self.assertEqual(answers, [str(DEGREE_SEEKING_FIRST_TIME_NON_FRESHMAN)])


    def test_ask_for_total_undergraduates_enrollment(self):
        question = "how many undergraduate students are enrolled?"
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
            createEntityObjHelper("undergraduate"),
        ],  2020, 2021))
        self.assertEqual(answers, [str(TOTAL_UNDERGRADUATES)])

    def test_ask_for_full_time_undergraduates_enrollment(self):
        question = "what is the full-time undergraduate enrollment?"
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
            createEntityObjHelper("undergraduate"),
            createEntityObjHelper("full-time")], 2020, 2021))
        self.assertEqual(answers, [str(TOTAL_UNDERGRADUATES - TOTAL_UNDERGRADUATE_PART_TIME)])


    def test_ask_for_data_for_invalid_year_should_throw_error(self):
       
        with self.assertRaises(NoDataFoundException) as cm:
            question = "what is the full-time undergraduate enrollment?"
            asyncio.run(self.knowledgeBase.searchForAnswer(question, "enrollment", [
                createEntityObjHelper("african american"),
            ],  3000, 3001))
            
        exceptionRaised = cm.exception
        self.assertEqual(exceptionRaised.fallBackMessage,
                             NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=3000, end=3001))
        self.assertEqual(exceptionRaised.type,
                             ExceptionTypes.NoDataFoundForAcademicYearException)

class Question_answer_knowledgebase_test(unittest.TestCase):
    def setUp(self):
        self.databaseName = "CDS_2020_2021"
        f = open('./tests/testMaterials/cdsTestData/CDS_2020_2021.json')
        self.data = json.load(f)
        f.close()

        with patch('pymongo.MongoClient') as mockClient:
            self.mockClient = mockClient
            self.mockDataSource(mockClient)
        
        # mockClient.list_database_names.return_value = 
      
        mongoProcessor = MongoProcessor()
        mongoProcessor = ConvertToDocumentDecorator(mongoProcessor)
        mongoDataManager = MongoDataManager(mongoProcessor, mockClient)
      
        self.questionAnswerKnowledgebase = QuestionAnswerKnowledgeBase(mongoDataManager)
        asyncio.run(self.questionAnswerKnowledgebase.initialize())
        
        


    def mockDataSource(self, mockClient): 
   
        mockClient.list_database_names.return_value = [self.databaseName]
        sections = self.data["sections"]
        mockClient[self.databaseName].list_collection_names.return_value = sections
        index = 0
        def sideEffect(filter : Dict[str, any]):
            # print("TEST_________________________________---")
            # print(mockClient.mock_calls)
        
            # for sectionName in sections: 
            #     if sectionName == section:
            #         break

            #     index = index+1
            nonlocal index
            data = self.data["data"][index]
            index = index + 1
            return data

        self.mockClient[self.databaseName][any].find.side_effect = sideEffect
      
        # print("FOUND _____")
        # print(mockClient[databaseName]["test"].find())
     
    def test_ask_about_student_to_faculty_ratio_should_return_correct_answer(self):
        
        question = "What is the student to faculty ratio?"
        intent = "faculty and class size"
        answer = "The student to faculty ratio is 10 to 1"
        entities = []
        
        chatbotAnswers, shouldContinue = asyncio.run(self.questionAnswerKnowledgebase.searchForAnswer(question, intent, entities, "2020","2021"))
        answers : List[str] = testUtils.getAnswers(chatbotAnswers=chatbotAnswers)
        self.assertIn(answer, answers)

    def test_ask_about_undergraduate_tuition_should_return_correct_answer(self):
        
        question = "What is cost of undergraduate tuition?"
        intent = "annual expense"
        answer = "Rose-Hulman's tuition for undergraduate students is $49,479"
        entities = []
        
        chatbotAnswers, shouldContinue = asyncio.run(self.questionAnswerKnowledgebase.searchForAnswer(question, intent, entities, "2020","2021"))
        answers : List[str] = testUtils.getAnswers(chatbotAnswers=chatbotAnswers)
        self.assertIn(answer, answers)

    


    


if __name__ == '__main__':
    unittest.main()
