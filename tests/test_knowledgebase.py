

import asyncio
from copy import deepcopy
from typing import List
import unittest
import os
import sys
import Data_Ingestion.constants as metadataConstants
import tests.testUtils as testUtils
from Knowledgebase.DataModels.SearchResult import SearchResult


from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
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

class knowledgebase_test(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
