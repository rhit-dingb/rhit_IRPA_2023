
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
from tests.testUtils import checkAnswersMatch, checkForKeywordInAnswer, createEntityObjHelper, createFakeTracker, identityFunc
from actions.actions import  ActionQueryKnowledgebase, knowledgeBase as knowledgeBaseInAction
from actions.actions import ActionQueryCohort

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from student life in 2020-2021 CDS data
PERCENT_UNDERGRADUATE_JOIN_FRATERNITY = "32.5%"
PERCENT_FRESHMAN_JOIN_FRATERNITY = "22.9%"
class test_student_life(unittest.TestCase):
    def setUp(self):
        self.intent = "student_life"
        # These should be intents
        self.topicToParse = [self.intent]
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials/cdsTestData", self.topicToParse))
     
        self.dispatcher = CollectingDispatcher()
        #Make sure the knowledgebase class instance in Actions is using the data manager with test materials loaded.
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        knowledgeBaseInAction.constructOutput = identityFunc
        
              
    def test_when_ask_student_join_fraternity_should_return_freshman_and_undergraduate_percentage(self):
        entities =  [
               createEntityObjHelper("fraternity")
        ]
        actionStudentLife = ActionQueryKnowledgebase()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionStudentLife.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswerKeywords = [PERCENT_UNDERGRADUATE_JOIN_FRATERNITY,PERCENT_FRESHMAN_JOIN_FRATERNITY]
        checkForKeywordInAnswer(self, self.dispatcher, expectedAnswerKeywords)
        
        
    


if __name__ == '__main__':
    unittest.main()
