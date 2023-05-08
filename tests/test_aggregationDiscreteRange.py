
import asyncio
import unittest
from unittest import mock
from unittest.mock import patch
from DataManager.constants import *
from Knowledgebase.Knowledgebase import KnowledgeBase

from Knowledgebase.SparseMatrixKnowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.SparseMatrixKnowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from tests.testUtils import checkAnswersMatch, createEntityObjHelper, createFakeTracker, extractOutput

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#These values are from student life in 2020-2021 CDS data

ACT_SCORE_INTENT = "act score"
class test_aggregationDiscreteRange(unittest.TestCase):
    def setUp(self):


       
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials/testForDiscreteRange/"))
        self.defaultShouldAddRowStrategy = DefaultShouldAddRowStrategy()
      
        self.knowledgeBase.getAllEntityForRealQuestionFoundForAnswer = self.fakeGetAllEntityForRealQuestionFoundForAnswer
        self.extractOutput = extractOutput
        self.knowledgeBase.constructOutput = self.extractOutput

    async def fakeGetAllEntityForRealQuestionFoundForAnswer(self, searchResults):
        pass

    def test_when_ask_for_student_with_act_score_with_upper_bound_should_return_correct_answer(self):
        intent = ACT_SCORE_INTENT
        entities =  [
            createEntityObjHelper("act"),
            createEntityObjHelper("within", entityLabel=RANGE_ENTITY_LABEL),
            createEntityObjHelper("30", entityLabel = NUMBER_ENTITY_LABEL)
        ]

        # intent, entities, sparseMatrix : SparseMatrix, isSumming
        # sparseMatrix, startYear, endYear = self.knowledgeBase.determineMatrixToSearch(intent, entities)
        # rangeResultData = self.knowledgeBase.aggregateDiscreteRange(ACT_SCORE_INTENT, entities, sparseMatrix ,True )
        # answers = rangeResultData.answers
        question = "Number of act score within 30"
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, intent, entities, 2021, 2022))
        self.assertEqual(answers, [str(11)])

    def test_when_ask_for_student_with_act_score_with_upper_bound_and_lower_bound_should_return_correct_answer(self):
        intent = ACT_SCORE_INTENT
        question = "Number of act with score more than 6 and within 22"
        entities =  [
            createEntityObjHelper("act"),
            createEntityObjHelper("within"),
            createEntityObjHelper("more than", entityLabel= RANGE_ENTITY_LABEL),
            createEntityObjHelper("22", entityLabel = NUMBER_ENTITY_LABEL),
            createEntityObjHelper("6", entityLabel = NUMBER_ENTITY_LABEL)
        ]

        # sparseMatrix, startYear, endYear = self.knowledgeBase.determineMatrixToSearch(intent, entities, self.knowledgeBase.year)
        # rangeResultData = self.knowledgeBase.aggregateDiscreteRange(ACT_SCORE_INTENT, entities, sparseMatrix ,True )
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question, intent, entities, 2021, 2022))
        self.assertEqual(answers, [str(6)])


if __name__ == '__main__':
    unittest.main()
