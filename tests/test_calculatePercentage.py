
import asyncio
from typing import List
import unittest
from unittest import mock
from unittest.mock import patch
from DataManager.constants import *
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.Knowledgebase import KnowledgeBase

from Knowledgebase.SparseMatrixKnowledgeBase import SparseMatrixKnowledgeBase
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from DataManager.ExcelDataManager import ExcelDataManager
from OutputController import output
from tests.testUtils import checkAnswersMatch, createEntityObjHelper, createFakeTracker, extractOutput

#These values are from student life in 2020-2021 CDS data

ACT_SCORE_INTENT = "act score"
class test_aggregationDiscreteRange(unittest.TestCase):
    def setUp(self):
      
        self.knowledgeBase = SparseMatrixKnowledgeBase(
            ExcelDataManager("./tests/testMaterials/cdsTestData"))
        self.knowledgeBase.getAllEntityForRealQuestionFoundForAnswer = self.fakeGetAllEntityForRealQuestionFoundForAnswer
        self.extractOutput = extractOutput
       
        self.mockRasaCommunicator = None
        with patch('Parser.RasaCommunicator') as mockRasaCommunicator:
            self.mockRasaCommunicator = mockRasaCommunicator
            self.knowledgeBase.rasaCommunicator = mockRasaCommunicator
            print(self.mockRasaCommunicator)

    def getAnswers(self, answers: List[ChatbotAnswer]):
        ans = []
        for answer in answers:
            ans.append(answer.answer)
        return ans

    async def fakeGetAllEntityForRealQuestionFoundForAnswer(self, searchResults):
        pass

    def test_ask_percentage_of_male_students(self):
        fake_return_value = {
            "intent": {
              "name": "enrollment"
            },
            "entities": [
            ]
        }

        entities = [
            createEntityObjHelper("male", "gender"),
            createEntityObjHelper("percent", "aggregation")

        ]
        question = "What is the percentage of male students"
        # mock async call
        f = asyncio.Future()
        f.set_result(fake_return_value)
        self.mockRasaCommunicator.parseMessage.return_value=f
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question,"enrollment", entities, 2020, 2021, completeSentence=False))
        answers = self.getAnswers(answers)
        self.assertEqual(answers, ["76.0%"])

    def test_ask_percentage_of_male_students(self):
        fake_return_value = {
            "intent": {
              "name": "enrollment"
            },
            "entities": [
            ]
        }

        entities = [
            createEntityObjHelper("female", "gender"),
            createEntityObjHelper("percent", "aggregation")

        ]
        question = "What is the percentage of female students"
        # mock async call
        f = asyncio.Future()
        f.set_result(fake_return_value)
        self.mockRasaCommunicator.parseMessage.return_value=f
        answers, shouldContinue = asyncio.run(self.knowledgeBase.searchForAnswer(question,"enrollment", entities, 2020, 2021, completeSentence=False))
        answers = self.getAnswers(answers)
        self.assertEqual(answers, ["24.0%"])


    