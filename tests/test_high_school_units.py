
import unittest
from unittest import mock
from unittest.mock import patch
from DataManager.constants import *
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_COHORT_YEAR_ERROR_MESSAGE_FORMAT
from Knowledgebase.Knowledgebase import KnowledgeBase

from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.ChooseFromOptionsAddRowStrategy import ChooseFromOptionsAddRowStrategy
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from OutputController import output
from tests.testUtils import createEntityObjHelper, createFakeTracker, identityFunc
from actions.actions import ActionQueryHighSchoolUnits, knowledgeBase as knowledgeBaseInAction
from actions.actions import ActionQueryCohort

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from the high school unit sheet dataset in 2020-2021 CDS data
LAB_SCIENCE_UNIT_REQUIRED = 3
VISUAL_PERFORMING_ART_UNIT_RECOMMENDED = 0
TOTAL_REQUIRED_UNITS = 16
TOTAL_RECOMMENDED_UNITS = 13
class test_high_school_units_test(unittest.TestCase):
    def setUp(self):
        
        self.intent = "high_school_units"
        # These should be intents
        self.topicToParse = ["enrollment", "cohort", "high_school_units"]
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials", self.topicToParse))
     

        self.dispatcher = CollectingDispatcher()
        #Make sure the knowledgebase class instance in Actions is using the data manager with test materials loaded.
        knowledgeBaseInAction.dataManager = self.knowledgeBase.dataManager
        output.constructSentence = identityFunc
        output.outputFuncForHighSchoolUnits = identityFunc

        
    def test_when_ask_lab_science_unit_required_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("lab"),
                createEntityObjHelper("science"),
                createEntityObjHelper("units-required"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]
         
        actionHighSchool = ActionQueryHighSchoolUnits()
        dispatcher = CollectingDispatcher()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=dispatcher, tracker=tracker, domain=None )
        self.assertEqual(dispatcher.messages[0]["text"],LAB_SCIENCE_UNIT_REQUIRED)

    def test_when_ask_visual_performing_art_recommended_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("visual/performing-arts"),
                createEntityObjHelper("units-recommended"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]

        actionHighSchool = ActionQueryHighSchoolUnits()
        dispatcher = CollectingDispatcher()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=dispatcher, tracker=tracker, domain=None )
        
        self.assertEqual(dispatcher.messages[0]["text"],VISUAL_PERFORMING_ART_UNIT_RECOMMENDED)
    
    
    def test_when_ask_total_units_required_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("units-required"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]

        actionHighSchool = ActionQueryHighSchoolUnits()
        dispatcher = CollectingDispatcher()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=dispatcher, tracker=tracker, domain=None )
        
        self.assertEqual(dispatcher.messages[0]["text"], TOTAL_REQUIRED_UNITS)
        
    def test_when_ask_total_units_recommended_should_return_correct_value(self):
        entities =  [
                createEntityObjHelper("units-recommended"),
                createEntityObjHelper("2020", "year", "from"),
                createEntityObjHelper("2021", "year", "to")
            ]

        actionHighSchool = ActionQueryHighSchoolUnits()
        dispatcher = CollectingDispatcher()
        tracker = Tracker.from_dict(createFakeTracker(self.intent, entities))
        actionHighSchool.run(dispatcher=dispatcher, tracker=tracker, domain=None )
        
        self.assertEqual(dispatcher.messages[0]["text"],TOTAL_RECOMMENDED_UNITS)
    


if __name__ == '__main__':
    unittest.main()
