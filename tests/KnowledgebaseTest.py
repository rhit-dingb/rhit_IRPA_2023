
import unittest
import os
import sys
sys.path.append('..')
from Data_Ingestion.ExcelProcessor import ExcelProcessor
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase

TOTAL_UNDERGRADUATES = 1972
TOTAL_GRADUATES = 21
class SparseMatrixKnowledgebaseTest_Enrollment (unittest.TestCase):
    def setUp(self):
        
        self.knowledgeBase = SparseMatrixKnowledgeBase("../Data_Ingestion/CDS_SPARSE_ENR.xlsx")
        self.excelProcessor = ExcelProcessor()
        self.topicToParse = ["General_Enrollment"]
        self.data = self.excelProcessor.processExcelSparse("../Data_Ingestion/CDS_SPARSE_ENR.xlsx", self.topicToParse)
        self.m_df = self.data["General_Enrollment"]
        #Making sure the data is consistent for testing
        self.knowledgeBase.m_df = self.m_df
        
        
    def test_when_ask_for_total_undergraduates_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["undergraduate"])
        self.assertEqual(answer, str(TOTAL_UNDERGRADUATES))

    def test_when_ask_for_total_graduates_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", ["graduate"])
        self.assertEqual(answer, str(TOTAL_GRADUATES))
        

if __name__ == '__main__':
    unittest.main()
