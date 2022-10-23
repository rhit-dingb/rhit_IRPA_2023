from copy import deepcopy
import unittest
from DataManager.constants import COHORT_BY_YEAR_ENTITY_LABEL
from Knowledgebase.Knowledgebase import KnowledgeBase

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
from actions.actions import *


#These values are from the 2014 cohort in the 2013-2014 dataset 
INITIAL_2014_COHORT_TOTAL = 582


class cohort_test(unittest.TestCase):
    def setUp(self):
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
    def test_knowledgebase_when_ask_for_initial_cohort_should_return_correct_value(self):
        answer = self.knowledgeBase.searchForAnswer(
            "cohort",
            [
            createEntityObjHelper("initial"),
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL)
            ], self.defaultShouldAddRowStrategy
        )

        self.assertEqual(answer, str(INITIAL_2014_COHORT_TOTAL))

    def test_when_ask_for_graduation_time_five_to_six_year_should_give_correct_value(self):
        answer = self.knowledgeBase.searchForAnswer(
            "cohort",
            [
            createEntityObjHelper("initial"),
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper("", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL)
            
            ], self.defaultShouldAddRowStrategy
        )

        # knowledgeBase = 
        # queryCohort = ActionQueryCohort()

        #self.assertEqual(answer, str(INITIAL_2014_COHORT_TOTAL))



if __name__ == '__main__':
    unittest.main()
