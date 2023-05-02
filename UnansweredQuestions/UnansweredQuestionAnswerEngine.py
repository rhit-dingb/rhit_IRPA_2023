



from typing import List
from UnansweredQuestions.DocumentRetrieverByVector import DocumentRetrieverByVector
from UnansweredQuestions.MongoDBUnansweredQuestionConnector import MongoDBUnansweredQuestionConnector
from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.DocumentIndexRetriever import DocumentIndexRetriever
from UnansweredQuestions.TFIDFModel import TFIDFModel
from UnansweredQuestions.Word2Vec import Word2VecModel
from UnansweredQuestions.constants import DB_UNANSWERED_QUESTION_QUESTION_FIELD_KEY
from UnansweredQuestions.constants import DB_UNANSWERED_QUESTION_ANSWER_FIELD_KEY
from UnansweredQuestions.UnasweredQuestionDBConnector import UnansweredQuestionDbConnector
from UnansweredQuestions import Model

import sys
import os




   #self.model = TFIDFModel(self.corpus, "./savedModels/tfidf.tfidf")

class UnansweredQuestionAnswerEngine:
    # Basepath: ./UnansweredQuestions, or ../UnansweredQuestions
    def __init__(self, databaseConnector : UnansweredQuestionDbConnector):
        self.modelToUse = None
        self.dbConnector = databaseConnector
        basePath = self.determinePath()
        self.corpus = Corpus(self.dbConnector,  basePath +"/dictionaries/dictionary")
        self.model : Model = Word2VecModel(self.corpus, basePath +"/savedModels/wordVectorModel")
        # self.model.initializeModel()
        self.documentRetriever = DocumentIndexRetriever(self.corpus, self.model, basePath +"/indexes/unansweredQuestion.index")
        self.update()
        self.confidenceThreshold = 0.9
       # self.documentRetriever= DocumentRetrieverByVector(self.corpus, self.wordToVecModel)
    

    def determinePath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        unansweredQues_dir = os.path.join(base_dir, "UnansweredQuestions")
        return unansweredQues_dir 

    def update(self):
        print("UPDATE CALLED")
        self.corpus.update()
        self.documentRetriever.update()
        # print("UPDATED")
        #maybe train the model here

    def questionDeleted(self, questionDeletedId):
        print("QUESTION DELETED")
        self.update()

    def questionAnswered(self, questionAnsweredId):
        self.update()
        print("QUESTION ANSWERED")
        questionObj = self.dbConnector.getQuestionAnswerObjectById(questionAnsweredId)
        questionAnswered = questionObj[DB_UNANSWERED_QUESTION_QUESTION_FIELD_KEY]
        answer = questionObj[DB_UNANSWERED_QUESTION_ANSWER_FIELD_KEY]
        self.model.trainModel([questionAnswered])



    def answerQuestion(self,question) -> List[str]:
        answers, confidences = self.documentRetriever.findSimilarDocuments(query=question)
        answersToReturn = []

        print("SEARCHING FOR QUESTION")
        # print(answersToReturn)
        print(confidences)
        print(answers)
        for answer, confidence in zip(answers, confidences):
            # print("CONFIDENCE")
            # print(confidence)
            if confidence >=self.confidenceThreshold:
                answersToReturn.append(answer)
        
        return answersToReturn
   
   




