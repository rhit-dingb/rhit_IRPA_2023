import unittest
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch
from UnansweredQuestions.UnansweredQuestionAnswerEngine import UnansweredQuestionAnswerEngine
from UnansweredQuestions.MongoDBUnansweredQuestionConnector import MongoDBUnansweredQuestionConnector
from UnansweredQuestions.UnasweredQuestionDBConnector import UnansweredQuestionDbConnector
import json

from UnansweredQuestions.constants import DB_UNANSWERED_QUESTION_IS_ADDRESSED_FIELD_KEY, DB_UNANSWERED_QUESTION_ANSWER_FIELD_KEY


class test_unansweredQuestionEngine(unittest.TestCase):
    def setUp(self):
        # self.unansweredQuestionDbConnector : UnansweredQuestionDbConnector = MongoDBUnansweredQuestionConnector()
        f = open('./tests/testMaterials/unansweredQuestionTestMaterial/unansweredQuestionsData.json')
        self.testData = json.load(f)
        f.close()
        self.answeredQuestion =  self.getAllAnsweredQuestionHelper()
        
        # self.unansweredQuestionAnswerEngine = UnansweredQuestionAnswerEngine(self.unansweredQuestionDbConnector)

    @patch('UnansweredQuestions.MongoDBUnansweredQuestionConnector')
    # @patch('UnansweredQuestions.UnansweredQuestionAnswerEngine.UnansweredQuestionAnswerEngine.update', return_value='mocked value')
    def test_ask_question_should_return_correct_answer_for_unanswered_question(self,  mockDb):
        # unansweredQuestionDbConnector : UnansweredQuestionDbConnector = MongoDBUnansweredQuestionConnector()
        # print(unansweredQuestionDbConnector.getAllUnansweredQuestionAndAnswer())
        self.mockDbReturnValues(mockDb)
        unansweredQuestionAnswerEngine = UnansweredQuestionAnswerEngine(mockDb)
        questionToAsk = "What is the trend in admission?"
        answer = self.testData[0][DB_UNANSWERED_QUESTION_ANSWER_FIELD_KEY]
        answers = unansweredQuestionAnswerEngine.answerQuestion(questionToAsk)
        self.assertEquals(answer, answers[0])



    @patch('UnansweredQuestions.MongoDBUnansweredQuestionConnector')
    # @patch('UnansweredQuestions.UnansweredQuestionAnswerEngine.UnansweredQuestionAnswerEngine.update', return_value='mocked value')
    def test_ask_question_with_low_confidence_should_return_no_answer(self,  mockDb):
        # unansweredQuestionDbConnector : UnansweredQuestionDbConnector = MongoDBUnansweredQuestionConnector()
        # print(unansweredQuestionDbConnector.getAllUnansweredQuestionAndAnswer())
        self.mockDbReturnValues(mockDb)
        unansweredQuestionAnswerEngine = UnansweredQuestionAnswerEngine(mockDb)
        questionToAsk = "What is the largest animal in the world?"
        answers = unansweredQuestionAnswerEngine.answerQuestion(questionToAsk)
        self.assertEqual([],answers)

    @patch('UnansweredQuestions.Corpus')
    @patch('UnansweredQuestions.Model')
    @patch('UnansweredQuestions.MongoDBUnansweredQuestionConnector')
    def test_answer_question_should_update_corpus_and_model(self,mockDb, mockModel, mockCorpus):
        self.mockDbReturnValues(mockDb)
        unansweredQuestionAnswerEngine = UnansweredQuestionAnswerEngine(mockDb)
        unansweredQuestionAnswerEngine.corpus = mockCorpus
        unansweredQuestionAnswerEngine.model = mockModel
        unansweredQuestionAnswerEngine.questionAnswered( self.testData[1]["_id"])
        mockCorpus.update.assert_called_once()
        mockModel.trainModel.assert_called_once()


    
    def mockDbReturnValues(self, mockDb):
        mockDb.getAllUnansweredQuestionAndAnswers.return_value = self.testData
        mockDb.getAnsweredQuestionSortedByDate.return_value = self.answeredQuestion

    def getAllAnsweredQuestionHelper(self):
        data = []
        for questionAnswerObj in self.testData:
            if questionAnswerObj[DB_UNANSWERED_QUESTION_IS_ADDRESSED_FIELD_KEY] == True:
                data.append(questionAnswerObj)
        
        return data
