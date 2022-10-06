
import unittest
import os
import sys


sys.path.append('..')
from Data_Ingestion.ExcelProcessor import ExcelProcessor
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.AllMustMatchAddRowStrategy import AllMustMatchAddRowStrategy


TOTAL_UNDERGRADUATES = 1972
TOTAL_UNDERGRADUATE_PART_TIME = 20
DEGREE_SEEKING_FIRST_TIME_FRESHMAN = 531
HISPANIC_STUDENTS_ENROLLMENT = 138
NON_FRESHMAN = 1459
DEGREE_SEEKING_FIRST_TIME_NON_FRESHMAN = 1100
TOTAL_GRADUATES = 21

class SparseMatrixKnowledgebaseTest_Enrollment (unittest.TestCase):
    def setUp(self):
        
        self.knowledgeBase = SparseMatrixKnowledgeBase("../Data_Ingestion/CDS_SPARSE_ENR.xlsx")
        self.excelProcessor = ExcelProcessor()
        self.topicToParse = ["enrollment"]
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
        self.allMustMatchStrategy = AllMustMatchAddRowStrategy()
        #Making sure the data loaded is consistent for testing
        self.data = self.excelProcessor.processExcelSparse("../Data_Ingestion/CDS_SPARSE_ENR.xlsx", self.topicToParse)
    
    def test_ask_for_total_undergraduates_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["undergraduate"], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(TOTAL_UNDERGRADUATES))

    def test_ask_for_full_time_undergraduates_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["undergraduate", "full-time"], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(TOTAL_UNDERGRADUATES-TOTAL_UNDERGRADUATE_PART_TIME))

    #degree-seeking, first_time, freshman/all other, first-year
    def test_ask_for_full_time_undergradutes_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["degree-seeking", "first-time", "freshman"], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(DEGREE_SEEKING_FIRST_TIME_FRESHMAN))
    
    def test_ask_for_hispanics_students_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["hispanic"], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(HISPANIC_STUDENTS_ENROLLMENT))

    def test_ask_for_non_freshmans(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["non-freshman"], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(NON_FRESHMAN))

    def test_ask_for_full_time_undergraduate_men_non_freshmans(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["full-time", "degree-seeking", "men", "non-freshman"], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(DEGREE_SEEKING_FIRST_TIME_NON_FRESHMAN))

    #for this test, I am assuming if we asked for data that the CDS does not have, the knowledge base default to zero.
    def test_ask_for_out_of_scope_data_should_return_zero(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["men", "asian"], self.allMustMatchStrategy)
        self.assertEqual(answer, str(0))
    
    def test_ask_for_african_american_first_time_first_year_degree_seeking(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["african-american", "first-year", "first-time", "degree-seeking"], self.allMustMatchStrategy)
        self.assertEqual(answer, str(0))

if __name__ == '__main__':
    unittest.main()
