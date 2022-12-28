

from copy import deepcopy
import unittest
import os
import sys


from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT
from unittest.mock import patch
from unittest import mock
from tests.testUtils import createEntityObjHelper


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

class enrollment_test(unittest.TestCase):
    def setUp(self):
        # self.knowledgeBase = SparseMatrixKnowledgeBase("../Data_Ingestion/CDS_SPARSE_ENR.xlsx")
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials/cdsTestData"))
        self.knowledgeBase.setYear(2020)
        self.topicToParse = ["enrollment"]
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
    
        # #Making sure the data loaded is consistent for testing
        # self.data = self.excelProcessor.processExcelSparse("../Data_Ingestion/CDS_SPARSE_ENR.xlsx", self.topicToParse)
    def extractOutput(self, answers, intent, entities):
        return answers
    
    # def test_give_no_entities_should_sum_up_everything(self):
    #     answers = self.knowledgeBase.searchForAnswer("enrollment", [
    #     ], self.defaultShouldAddRowStrategy, self.extractOutput)
    #     self.assertEqual(answers, [str(TOTAL_UNDERGRADUATES+TOTAL_GRADUATES)])

    
    def test_when_ask_for_total_graduates_enrollment_should_return_correct_value(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("graduate"),
        ], self.defaultShouldAddRowStrategy, self.extractOutput)
        
        self.assertEqual(answers, [str(TOTAL_GRADUATES)])


    def test_when_ask_for_non_degree_seeking_should_return_correct_value(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("non-degree-seeking"),
        ], self.defaultShouldAddRowStrategy, self.extractOutput)

        self.assertEqual(answers, [str(NON_DEGREE_SEEKING_STUDENTS)])

    def test_ask_for_full_time_undergraduate_men_non_freshmans(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("full-time"),
            createEntityObjHelper("degree-seeking"),
            createEntityObjHelper("male"),
            createEntityObjHelper("non-freshman"),
            ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(DEGREE_SEEKING_FIRST_TIME_NON_FRESHMAN)])


    def test_ask_for_total_undergraduates_enrollment(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("undergraduate"),
            createEntityObjHelper("2020", "year", "from"),
            createEntityObjHelper("2021", "year", "to")

        ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(TOTAL_UNDERGRADUATES)])

    def test_ask_for_full_time_undergraduates_enrollment(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("undergraduate"),
            createEntityObjHelper("2020", "year", "from"),
            createEntityObjHelper("2021", "year", "to"),
            createEntityObjHelper("full-time")], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(TOTAL_UNDERGRADUATES - TOTAL_UNDERGRADUATE_PART_TIME)])

    # degree-seeking, first_time, freshman/all other, first-year
    def test_ask_for_full_time_undergradutes_enrollment(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("degree-seeking"),
            createEntityObjHelper("first-time"),
            createEntityObjHelper("2020", "year", "from"),
            createEntityObjHelper("2021", "year", "to"),
            createEntityObjHelper("freshman")], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(DEGREE_SEEKING_FIRST_TIME_FRESHMAN)])


    def test_ask_for_non_freshmans(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment",
                                                    [
                                                        createEntityObjHelper(
                                                            "non-freshman")
                                                    ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(NON_FRESHMAN)])

 

    def test_ask_for_hispanics_students_enrollment(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("hispanic"),
        ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(HISPANIC_STUDENTS_ENROLLMENT)])


    # # for this test, I am assuming if we asked for data that the CDS does not have,
    # # the algorithm current will try to answers to its best of its ability.
    def test_ask_for_out_of_scope_data_should_answers_to_best_ability(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment",
                                                    [createEntityObjHelper("male"),
                                                     createEntityObjHelper("asian", entityLabel="race"), 
                                                    createEntityObjHelper("2020", "year", "from"),
                                                    createEntityObjHelper("2021", "year", "to")],
                                                    self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED)])



    # # It might be worth thinking about which matrix will be used for this test case compared to the previous test case.
    # # The entities in the above test case are mutually exclusive, meaning one exist in the first matrix(general enrollment) for enrollment while
    # # the second one exist in the second matrix(enrollment by race) for enrollment. So there will be a tie. For this case,
    # # degree-seeking exist in the first matrix but also the second, and "asian" exist only in the second matrix,
    # # since more entities are in the second matrix, the second matrix will be used.
    def test_ask_for_degree_seeking_asian_student_enrolled_should_return_degree_seeking_undergraduate_asian_students(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment",
                                                    [createEntityObjHelper("degree-seeking"),
                                                     createEntityObjHelper("asian")],
                                                    self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED)])

    def test_ask_for_african_american_first_time_first_year_degree_seeking(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [createEntityObjHelper("african american"),
                                                                   createEntityObjHelper(
                                                                       "first-year"),
                                                                   createEntityObjHelper(
                                                                       "first-time"),
                                                                   createEntityObjHelper("degree-seeking")], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(31)])

    def test_ask_for_asian_student_enrollment_should_not_sum_up_two_row(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("asian"),
        ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(
            DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED)])

    def test_ask_for_hispanic_enrollment_but_given_included_invalid_entity_should_return_only_hispanic_enrollment(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("hispanic"),
            createEntityObjHelper("pizza")
        ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(HISPANIC_STUDENTS_ENROLLMENT)])

    def test_ask_for_first_time_unknown_race_but_entity_provided_twice(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("unknown"),
            createEntityObjHelper("first-time"),
            createEntityObjHelper("first-time"),
        ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(
            UNDERGRADUATE_FIRST_TIME_DEGREE_SEEKING_UNKNOWN_RACE_STUDENT_ENROLLED)])

    def test_ask_for_african_american_student_enrollment(self):
        answers = self.knowledgeBase.searchForAnswer("enrollment", [
            createEntityObjHelper("african american"),
        ], self.defaultShouldAddRowStrategy, self.extractOutput)
        self.assertEqual(answers, [str(
            UNDERGRADUATE_DEGREE_SEEKING_AFRICAN_AMERICAN_STUDEN_ENROLLED)])

    def test_ask_for_data_for_invalid_year_should_throw_error(self):
        self.knowledgeBase.setYear(3000)
        with self.assertRaises(NoDataFoundException) as cm:
            self.knowledgeBase.searchForAnswer("enrollment", [
                createEntityObjHelper("african american"),
            ], self.defaultShouldAddRowStrategy, self.extractOutput)
            
        exceptionRaised = cm.exception
        self.assertEqual(exceptionRaised.fallBackMessage,
                             NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=3000, end=3001))
        self.assertEqual(exceptionRaised.type,
                             ExceptionTypes.NoDataFoundForAcademicYearException)
        self.knowledgeBase.setYear(2020)

    # def test_ask_for_data_for_give_end_year_with_no_data_should_throw_error_message(self):

    #     # remove 2019 data so it doesn't exist, and test that given 2020 year but with role "to", it shouldn't look up 2020 data
    #     # but should throw an error
    #     parsedData = deepcopy(
    #         self.knowledgeBase.dataManager.excelProcessor.data)
    #     yearToRemove = "2019_2020"
    #     if yearToRemove in parsedData:
    #         del parsedData[yearToRemove]

    #     with patch("Data_Ingestion.ExcelProcessor") as mock:
    #         mockExcelProcessor = mock.return_value
    #         mockExcelProcessor.getData.return_value = parsedData

    #         with self.assertRaises(NoDataFoundException) as cm:
    #             self.knowledgeBase.searchForAnswer("enrollment", [
    #                 createEntityObjHelper("degree-seeking"),
    #                 createEntityObjHelper("non-first-time"),
    #                 createEntityObjHelper("2020", "year", "to")
    #             ], self.defaultShouldAddRowStrategy, self.extractOutput)

    #         exceptionRaised = cm.exception
    #         self.assertEqual(exceptionRaised.fallBackMessage,
    #                          NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=2019, end=2020))
    #         self.assertEqual(exceptionRaised.type,
    #                          ExceptionTypes.NoDataFoundForAcademicYearException)

    #TODO: add a test case that test that the knowledege base should use the earliest year if more than two academic year entities are given

    #TODO: add a test case that test the knowledgebase will use the most recent data if no year is provided. Use mocking to mock the most recent year data,since that will change as we add more sparse matrix files.


   


if __name__ == '__main__':
    unittest.main()
