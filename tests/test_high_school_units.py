
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
from actions.actions import ActionQueryKnowledgebase, knowledgeBase as knowledgeBaseInAction
from actions.actions import ActionQueryCohort

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from the high school unit sheet dataset in 2020-2021 CDS data
LAB_SCIENCE_UNIT_REQUIRED = "3"
VISUAL_PERFORMING_ART_UNIT_RECOMMENDED = "0"
TOTAL_REQUIRED_UNITS = "13"
TOTAL_RECOMMENDED_UNITS = "13"
class test_high_school_units_test(unittest.TestCase):
    def setUp(self):
        
        self.intent = "high_school_units"
        # These should be intents
        self.topicToParse = ["enrollment", "cohort", "high_school_units"]
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials/cdsTestData/cdsTestData", self.topicToParse))
     

        self.dispatcher = CollectingDispatcher()
        #Make sure the knowledgebase class instance in Actions is using the data manager with test materials loaded.
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        # output.constructSentence = identityFunc
        # output.outputFuncForHighSchoolUnits = identityFunc
        knowledgeBaseInAction.constructOutput = identityFunc

        
    def test_when_ask_lab_science_unit_required_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("lab"),
                createEntityObjHelper("science"),
                createEntityObjHelper("unit"),
                createEntityObjHelper("require"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]
         
        actionHighSchool = ActionQueryKnowledgebase()
      
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )

        expectedAnswers = [LAB_SCIENCE_UNIT_REQUIRED]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
       
    def test_when_ask_visual_performing_art_recommended_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("visual/performing-arts"),
                createEntityObjHelper("unit"),
                createEntityObjHelper("recommend"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]

        actionHighSchool = ActionQueryKnowledgebase()
        
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )

        expectedAnswers = [VISUAL_PERFORMING_ART_UNIT_RECOMMENDED]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
        
    
    
    def test_when_ask_total_units_required_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("unit"),
                createEntityObjHelper("require"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]

        actionHighSchool = ActionQueryKnowledgebase()
        
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
       
        expectedAnswers = [TOTAL_REQUIRED_UNITS]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
        
    def test_when_ask_total_units_recommended_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("unit"),
                createEntityObjHelper("recommend"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]

        actionHighSchool = ActionQueryKnowledgebase()
        dispatcher = CollectingDispatcher()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=self.dispatcher, tracker=tracker, domain=None )
        
        expectedAnswers = [TOTAL_RECOMMENDED_UNITS]
        checkAnswersMatch(self.assertEqual, self.dispatcher, expectedAnswers) 
    


if __name__ == '__main__':
    unittest.main()
