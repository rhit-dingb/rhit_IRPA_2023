
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
from actions.actions import ActionQueryFreshmanProfile, ActionQueryHighSchoolUnits, knowledgeBase as knowledgeBaseInAction
from actions.actions import ActionQueryCohort

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from the freshman profile in 2020-2021 CDS data
PERCENT_SUBMIT_SAT = "65.9%"
ACT_COMPOSITE_50_PERCENTILE_SCORE = 31
ACT_MATH_50_PERCENTILE_SCORE = 31
ACT_ENGLISH_50_PERCENTILE_SCORE = 31.5
ACT_WRITING_50_PERCENTILE_SCORE = "None"
PERCENT_STUDENT_WITH_SAT_READING_WRITING_SCORE_IN_RANGE_700_800 = "27.1%"
PERCENT_GRADUATING_IN_TOP_HALF_OF_HIGH_SCHOOL_CLASS = "99%"
class test_freshman_profile(unittest.TestCase):
    def setUp(self):
        
        self.intent = "freshman_profile"
        # These should be intents
        self.topicToParse = [self.intent]
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials", self.topicToParse))
     

        self.dispatcher = CollectingDispatcher()
        #Make sure the knowledgebase class instance in Actions is using the data manager with test materials loaded.
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        knowledgeBaseInAction.constructOutput = identityFunc
              
    def test_when_ask_percent_submit_sat_should_return_correct_value(self):
        entities =  [
               createEntityObjHelper("sat"),
               createEntityObjHelper("percent"),
               createEntityObjHelper("submitted")
            ]

        actionQueryFreshmanProfile = ActionQueryFreshmanProfile()
        
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionQueryFreshmanProfile.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )

        expectedAnswers = [PERCENT_SUBMIT_SAT]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
    

    def test_when_ask_act_50th_percentile_score_should_return_correct_multiple_values(self):
        entities =  [
               createEntityObjHelper("act"),
               createEntityObjHelper("50th percentile"),
            ]

        actionQueryFreshmanProfile = ActionQueryFreshmanProfile()
        
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionQueryFreshmanProfile.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )

        expectedAnswers = [PERCENT_SUBMIT_SAT]
        print(self.dispatcher.messages)
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
     
    
    def test_when_ask_sat_700_to_800_score_range_score_should_return_correct_percentage(self):
        entities =  [
            createEntityObjHelper("sat"),
            createEntityObjHelper("700-800"),
            createEntityObjHelper("reading"),
            createEntityObjHelper("writing")
        ]

        actionQueryFreshmanProfile = ActionQueryFreshmanProfile()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionQueryFreshmanProfile.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [PERCENT_STUDENT_WITH_SAT_READING_WRITING_SCORE_IN_RANGE_700_800 ]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
     

    def test_when_ask_percent_in_top_half_of_high_school_graduating_class(self):
        entities =  [
            createEntityObjHelper("graduation"),
            createEntityObjHelper("top half"),
            createEntityObjHelper("high school")
        ]

        actionQueryFreshmanProfile = ActionQueryFreshmanProfile()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionQueryFreshmanProfile.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        expectedAnswers = [PERCENT_GRADUATING_IN_TOP_HALF_OF_HIGH_SCHOOL_CLASS]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
    


if __name__ == '__main__':
    unittest.main()
