
import unittest
import os
import sys
sys.path.append('..')
from Knowledgebase.ExcelKnowledgeBase import ExcelKnowledgeBase



class ExcelKnowledgebaseTest (unittest.TestCase):
    def setUp(self):
        self.excelKnowledgeBase = ExcelKnowledgeBase("../Data_Ingestion/CDS_SPARSE_ENR.xlsx")
        self.parsedData = {'enrollment': {'Undergraduate': {'Degree-seeking, first-time freshman': {'Full-Time': {'Men': 387, 'Woman': 143}, 'Part-time': {'Men': 1, 'Woman': 
0}}, 'Other first year, degree-seeking': {'Full-Time': {'Men': 9, 'Woman': 2}, 'Part-time': {'Men': 0, 'Woman': 0}}, 'All Other degree-seeking non-freshman': {'Full-Time': {'Men': 1082, 'Woman': 329}, 'Part-time': {'Men': 15, 'Woman': 1}}, 'Total degree-seeking': {'Full-Time': {'Men': 1478, 'Woman': 474}, 'Part-time': {'Men': 16, 'Woman': 1}}, 'All other undergraduates enrolled in credit courses ': {'Full-Time': {'Men': 0, 'Woman': 0}, 'Part-time': {'Men': 2, 'Woman': 1}}, 'Total undergraduates': {'Full-Time': {'Men': 1478, 'Woman': 474}, 'Part-time': {'Men': 18, 'Woman': 2}}}, 'Graduates': {'Degree-seeking, first-time': {'Full-Time': {'Men': 3, 'Woman': 0}, 'Part-time': {'Men': 2, 'Woman': 1}}, 'All other degree-seeking': {'Full-Time': {'Men': 6, 'Woman': 1}, 'Part-time': {'Men': 5, 'Woman': 0}}, 'All other graduates enrolled in credit courses ': {'Full-Time': {'Men': 0, 'Woman': 0}, 'Part-time': {'Men': 2, 'Woman': 1}}, 'Total graduates': {'Full-Time': {'Men': 9, 'Woman': 1}, 'Part-time': {'Men': 7, 'Woman': 1}}}, 'Nonresident alien': {'Degree-seeking First-time First year': 36, 'Degree-seeking Undergraduates': 226}, 'Hispanic': {'Degree-seeking First-time First year': 34, 'Degree-seeking Undergraduates': 104}, 'African American': {'Degree-seeking First-time First year': 31, 'Degree-seeking Undergraduates': 93}, 'White': {'Degree-seeking First-time First year': 356, 'Degree-seeking Undergraduates': 1295}, 'American Indian': {'Degree-seeking First-time First year': 1, 'Degree-seeking Undergraduates': 3}, 'Asian': {'Degree-seeking First-time First year': 36, 'Degree-seeking Undergraduates': 127}, 'Pacific Islander': {'Degree-seeking First-time First year': 0, 'Degree-seeking Undergraduates': 0}, 'Two or more races': {'Degree-seeking First-time First year': 31, 'Degree-seeking Undergraduates': 99}, 'Ethnicity Unknown': {'Degree-seeking First-time First year': 6, 'Degree-seeking Undergraduates': 22}, 'Total': {'Degree-seeking First-time First year': 531, 'Degree-seeking Undergraduates': 1969}}}

    # def test_search_answers(self):
    #     #     answer = knowledgeBase.searchForAnswer(
    #     #     "enrollment", ["full-time"], knowledgeBase.aggregateTotal)
    #     # options = knowledgeBase.getAvailableOptions(
    #     #     "enrollment", ["undergraduates"])
    #     # print(answer)
    #     # print(options)
    #     pass

    def test_when_process_data_in_excel_knowledgebase_should_have_correct_data(self):
        self.assertEqual(self.parsedData,self.excelKnowledgeBase.data)



if __name__ == '__main__':
    unittest.main()
