from copy import deepcopy
import json
import unittest
from DataManager.constants import COHORT_BY_YEAR_ENTITY_LABEL, COHORT_INTENT, INITIAL_COHORT_ENTITY_LABEL, LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL, UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL
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
from tests.testUtils import createEntityObjHelper, createFakeTracker
from actions.actions import knowledgeBase as knowledgeBaseInAction
from actions.actions import ActionQueryCohort
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from the 2014 cohort in the 2013-2014 dataset 
INITIAL_2014_COHORT_TOTAL = 582
COHORT_2014_STUDENT_GRADUATING_IN_MORE_THAN_4_YEARS_AND_IN_FIVE_OR_LESS = 49

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
        entities =  [
            createEntityObjHelper("initial", entityLabel=INITIAL_COHORT_ENTITY_LABEL),
            createEntityObjHelper("2014 cohort", entityLabel=COHORT_BY_YEAR_ENTITY_LABEL),
            createEntityObjHelper("more than 4 years", entityLabel=LOWER_BOUND_GRADUATION_TIME_ENTITY_LABEL),
            createEntityObjHelper("5 more less years", entityLabel=UPPER_BOUND_GRADUATION_TIME_ENTITY_LABEL)
            ]

        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        queryCohort = ActionQueryCohort()
        dispatcher = CollectingDispatcher()
        tracker = Tracker.from_dict(createFakeTracker(COHORT_INTENT, entities))
        queryCohort.run(dispatcher=dispatcher, tracker=tracker, domain=None )
        
        self.assertEquals(dispatcher.messages[0]["text"], str(COHORT_2014_STUDENT_GRADUATING_IN_MORE_THAN_4_YEARS_AND_IN_FIVE_OR_LESS))
        #self.assertEqual(answer, str(INITIAL_2014_COHORT_TOTAL))



if __name__ == '__main__':
    unittest.main()
