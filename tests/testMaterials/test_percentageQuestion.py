
import unittest
from unittest import mock
from unittest.mock import patch
from DataManager.constants import *
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_COHORT_YEAR_ERROR_MESSAGE_FORMAT
from Knowledgebase.Knowledgebase import KnowledgeBase

from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from OutputController import output
from tests.testUtils import checkAnswersMatch, createEntityObjHelper, createFakeTracker, identityFunc
from actions.actions import  ActionQueryKnowledgebase, knowledgeBase as knowledgeBaseInAction
from actions.actions import ActionQueryCohort

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from student life in 2020-2021 CDS data

ACT_SCORE_INTENT = "act score"
class test_percentQuestion(unittest.TestCase):
    def setUp(self):
        self.topicToParse =  [ACT_SCORE_INTENT]
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials/testForDiscreteRange/", self.topicToParse))
        knowledgeBaseInAction.setYear(2020)
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
        self.knowledgeBase.constructOutput = identityFunc
        
              
    def test_when_ask_for_student_with_act_score_with_upper_bound_should_return_correct_answer(self):
        intent = ACT_SCORE_INTENT
        entities =  [
            createEntityObjHelper("act"),
            createEntityObjHelper("within", entityLabel=RANGE_ENTITY_LABEL),
            createEntityObjHelper("30", entityLabel = NUMBER_ENTITY_LABEL)
        ]

        # intent, entities, sparseMatrix : SparseMatrix, isSumming
        sparseMatrix, startYear, endYear = self.knowledgeBase.determineMatrixToSearch(intent, entities, self.knowledgeBase.year)
        rangeResultData = self.knowledgeBase.aggregateDiscreteRange(ACT_SCORE_INTENT, entities, sparseMatrix ,True )
        answers = rangeResultData.answers
        self.assertEqual(answers, [str(11)])




if __name__ == '__main__':
    unittest.main()
