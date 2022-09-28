import unittest
import os
import sys
sys.path.append('..')
from Knowledgebase.Knowledgebase import KnowledgeBase
from Knowledgebase.ExcelKnowledgeBase import ExcelKnowledgeBase

# import pip
# pip.main(["install", "openpyxl"])

class ExcelKnowledgebaseTest (unittest.TestCase):
    

    def test_search_answers(self):
        pass

    def test_process_excel(self):
        knowledgeBase = ExcelKnowledgeBase("../Data_Ingestion/CDSData.xlsx")
        #print(os.listdir("../data_ingestion/SampleData2"))
        #print(knowledgeBase.data)
        #answer = knowledgeBase.searchForAnswer("enrollment", ["undergraduate","Degree-seeking, first-time freshmen", "full-time"])
        # print(answer)
        # print( knowledgeBase.aggregateTotal(answer)) 

        answer = knowledgeBase.searchForAnswer("enrollment", ["full-time"], knowledgeBase.aggregateTotal)
        options = knowledgeBase.getAvailableOptions("enrollment", ["undergraduates"])
        print(answer)
        print(options)
  
if __name__ == '__main__':
    unittest.main()