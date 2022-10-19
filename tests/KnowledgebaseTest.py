
from copy import deepcopy
import unittest
import os
import sys
from unittest import mock
from unittest.mock import patch


sys.path.append('..')
from DataManager.ExcelDataManager import ExcelDataManager

from Data_Ingestion.ExcelProcessor import ExcelProcessor
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.ChooseFromOptionsAddRowStrategy import ChooseFromOptionsAddRowStrategy



# These values are data from the 2020-2021 CDS dataset.
TOTAL_UNDERGRADUATES = 1972
TOTAL_UNDERGRADUATE_PART_TIME = 20
DEGREE_SEEKING_FIRST_TIME_FRESHMAN = 531
HISPANIC_STUDENTS_ENROLLMENT = 138
NON_FRESHMAN = 1459
DEGREE_SEEKING_FIRST_TIME_NON_FRESHMAN = 1100
TOTAL_GRADUATES = 18
DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED = 127
UNDERGRADUATE_DEGREE_SEEKING_HISPANIC_STUDENTS_ENROLLED = 104
UNDERGRADUATE_FIRST_TIME_DEGREE_SEEKING_UNKNOWN_RACE_STUDENT_ENROLLED = 6
UNDERGRADUATE_DEGREE_SEEKING_AFRICAN_AMERICAN_STUDEN_ENROLLED = 93
NO_DATA_FOR_GIVE_YEAR_ERROR_MESSAGE_FORMAT = "No data fround for given year range {start}-{end}"
NON_FIRST_TIME = 1969

class SparseMatrixKnowledgebaseTest_Enrollment (unittest.TestCase):
    def setUp(self):
        
        # self.knowledgeBase = SparseMatrixKnowledgeBase("../Data_Ingestion/CDS_SPARSE_ENR.xlsx")
        self.knowledgeBase = SparseMatrixKnowledgeBase(ExcelDataManager("./testMaterials"))
       
        self.topicToParse = ["enrollment"]
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
        self.chooseFromOptionAddRowStrategy = ChooseFromOptionsAddRowStrategy(choices=[{
            "columns": ["degree-seeking", "first-time", "first-year"]
        }, 
        {
            "columns": ["degree-seeking", "non-first-time", "non-first-year"],
            "isDefault":True
        }])


        # #Making sure the data loaded is consistent for testing
        # self.data = self.excelProcessor.processExcelSparse("../Data_Ingestion/CDS_SPARSE_ENR.xlsx", self.topicToParse)

    def test_when_ask_for_total_graduates_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
        self.createEntityObjHelper("graduate")
        ], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(TOTAL_GRADUATES))

    def test_ask_for_total_undergraduates_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
        self.createEntityObjHelper("undergraduate")
        ], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(TOTAL_UNDERGRADUATES))

    def test_ask_for_full_time_undergraduates_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
            self.createEntityObjHelper("undergraduate"), 
            self.createEntityObjHelper("full-time")], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(TOTAL_UNDERGRADUATES-TOTAL_UNDERGRADUATE_PART_TIME))

    #degree-seeking, first_time, freshman/all other, first-year
    def test_ask_for_full_time_undergradutes_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
        self.createEntityObjHelper("degree-seeking"), 
        self.createEntityObjHelper("first-time"), 
        self.createEntityObjHelper("freshman")], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(DEGREE_SEEKING_FIRST_TIME_FRESHMAN))
    
    def test_ask_for_hispanics_students_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
        self.createEntityObjHelper("hispanic")
        ], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(HISPANIC_STUDENTS_ENROLLMENT))

    def test_ask_for_non_freshmans(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", 
        [
        self.createEntityObjHelper("non-freshman")
        ], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(NON_FRESHMAN))


    def test_ask_for_full_time_undergraduate_men_non_freshmans(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
            self.createEntityObjHelper("full-time"), 
            self.createEntityObjHelper("degree-seeking"), 
            self.createEntityObjHelper("men"), 
            self.createEntityObjHelper("non-freshman")], self.defaultShouldAddRowStrategy)
        self.assertEqual(answer, str(DEGREE_SEEKING_FIRST_TIME_NON_FRESHMAN))

    #for this test, I am assuming if we asked for data that the CDS does not have, 
    # the algorithm current will try to answer to its best of its ability.
    def test_ask_for_out_of_scope_data_should_answer_to_best_ability(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", 
        [self.createEntityObjHelper("men"), 
        self.createEntityObjHelper("asian")], 
        self.chooseFromOptionAddRowStrategy)
        
        self.assertEqual(answer, str(DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED))

    #It might be worth thinking about which matrix will be used for this test case compared to the previous test case.
    #The entities in the above test case are mutually exclusive, meaning one exist in the first matrix(general enrollment) for enrollment while
    # the second one exist in the second matrix(enrollment by race) for enrollment. So there will be a tie. For this case,
    # degree-seeking exist in the first matrix but also the second, and "asian" exist only in the second matrix,
    # since more entities are in the second matrix, the second matrix will be used.
    def test_ask_for_degree_seeking_asian_student_enrolled_should_return_degree_seeking_undergraduate_asian_students(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", 
        [self.createEntityObjHelper("degree-seeking"), 
        self.createEntityObjHelper("asian")], 
        self.chooseFromOptionAddRowStrategy)
        self.assertEqual(answer, str(DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED))
    
    def test_ask_for_african_american_first_time_first_year_degree_seeking(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [self.createEntityObjHelper("african-american"), 
        self.createEntityObjHelper("first-year"),
        self.createEntityObjHelper("first-time"), 
        self.createEntityObjHelper("degree-seeking")], self.chooseFromOptionAddRowStrategy)
        self.assertEqual(answer, str(31))

    def test_ask_for_asian_student_enrollment_should_not_sum_up_two_row(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
        self.createEntityObjHelper("asian")
        ], self.chooseFromOptionAddRowStrategy)
        self.assertEqual(answer, str(DEGREE_SEEKING_UNDERGRADUATE_ASIAN_STUDENTS_ENROLLED))
          
    def test_ask_for_hispanic_enrollment_but_given_included_invalid_entity_should_return_only_hispanic_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
            self.createEntityObjHelper("hispanic"), 
            self.createEntityObjHelper("pizza")
        ], self.chooseFromOptionAddRowStrategy)
        self.assertEqual(answer, str(104))

    def test_ask_for_first_time_unknown_race_but_entity_provided_twice(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
            self.createEntityObjHelper("unknown"), 
            self.createEntityObjHelper("first-time"),
            self.createEntityObjHelper("first-time")
        ], self.chooseFromOptionAddRowStrategy)
        self.assertEqual(answer, str(UNDERGRADUATE_FIRST_TIME_DEGREE_SEEKING_UNKNOWN_RACE_STUDENT_ENROLLED))

    def test_ask_for_african_american_student_enrollment(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
            self.createEntityObjHelper("african-american"), 
        ], self.chooseFromOptionAddRowStrategy)
        self.assertEqual(answer, str(UNDERGRADUATE_DEGREE_SEEKING_AFRICAN_AMERICAN_STUDEN_ENROLLED))


    def test_ask_for_data_for_invalid_year_should_return_error_message(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
            self.createEntityObjHelper("african-american"), 
             self.createEntityObjHelper("3000-3001", "year")
        ], self.chooseFromOptionAddRowStrategy)

        self.assertEqual(answer, NO_DATA_FOR_GIVE_YEAR_ERROR_MESSAGE_FORMAT.format(start = 3000, end = 3001))

    def test_ask_for_data_for_give_start_year_should_return_correct_data(self):
        answer = self.knowledgeBase.searchForAnswer("enrollment", [
            self.createEntityObjHelper("degree-seeking"),
            self.createEntityObjHelper("non-first-time"),
            self.createEntityObjHelper("2020","year", "from")
        ], self.defaultShouldAddRowStrategy)
     
        self.assertEqual(answer, str(NON_FIRST_TIME))

    
    def test_ask_for_data_for_give_end_year_with_no_data_should_return_error_message(self):

        # remove 2019 data so it doesn't exist, and test that given 2020 year but with role "to", it shouldn't look up 2020 data 
        # but instead return an error message.
        parsedData = deepcopy(self.knowledgeBase.dataManager.excelProcessor.data)
        yearToRemove = "2019_2020"
        if  yearToRemove in parsedData:
            del parsedData[yearToRemove]

        with patch("Data_Ingestion.ExcelProcessor") as mock:
            mockExcelProcessor = mock.return_value
            mockExcelProcessor.getData.return_value = parsedData
            answer = self.knowledgeBase.searchForAnswer("enrollment", [
                self.createEntityObjHelper("degree-seeking"),
                self.createEntityObjHelper("non-first-time"),
                self.createEntityObjHelper("2020","year", "to")
            ], self.defaultShouldAddRowStrategy)
        
            self.assertEqual(answer, str(NO_DATA_FOR_GIVE_YEAR_ERROR_MESSAGE_FORMAT.format(start = 2019, end =2020)))

    def createEntityObjHelper(self, entityValue, entityLabel="none",  entityRole = None):
        # we set the value of the entity key to any for now.
        res =  {"entity": entityLabel, "value":entityValue}
        if(entityRole):
            res["role"] = entityRole

        return res 

if __name__ == '__main__':
    unittest.main()
