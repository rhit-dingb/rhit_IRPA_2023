from copy import deepcopy
import unittest
import os
import sys
from DataManager.constants import COHORT_BY_YEAR_ENTITY_LABEL

from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.ChooseFromOptionsAddRowStrategy import ChooseFromOptionsAddRowStrategy
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT
from unittest.mock import patch
from unittest import mock

from tests.testUtils import createEntityObjHelper


#These values are from the 2014 cohort in the 2013-2014 dataset 
INITIAL_2014_COHORT_TOTAL = 582


class SparseMatrixKnowledgebaseTest_Cohort(unittest.TestCase):
    def setUp(self):
        print("SS")
        self.topicToParse = ["enrollment", "cohort"]
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials", self.topicToParse))

        
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
        self.chooseFromOptionAddRowStrategy = ChooseFromOptionsAddRowStrategy(choices=[{
            "columns": ["degree-seeking", "first-time", "first-year"]
        },
            {
            "columns": ["degree-seeking", "non-first-time", "non-first-year"],
            "isDefault":True
        }])

       
    #Cohorts actually uses the label of the entities.
    def test_when_ask_for_initial_cohort_should_return_correct_value(self):
        answer = self.knowledgeBase.searchForAnswer(
            "cohort",
            [
            createEntityObjHelper("initial"),
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL)
            ], self.defaultShouldAddRowStrategy
        )

        self.assertEqual(answer, str(INITIAL_2014_COHORT_TOTAL))



if __name__ == '__main__':
    unittest.main()
