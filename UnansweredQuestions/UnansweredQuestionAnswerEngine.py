



from typing import List
from UnansweredQuestions.DocumentRetrieverByVector import DocumentRetrieverByVector
from UnansweredQuestions.MongoDBUnansweredQuestionConnector import MongoDBUnansweredQuestionConnector
from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.Doc2Vec import Doc2VecModel
from UnansweredQuestions.DocumentIndexRetriever import DocumentIndexRetriever
from UnansweredQuestions.TFIDFModel import TFIDFModel
from UnansweredQuestions.Word2Vec import Word2VecModel
import sys
import os


class UnansweredQuestionAnswerEngine:
    # Basepath: ./UnansweredQuestions, or ../UnansweredQuestions
    def __init__(self, basePath : str):
        self.modelToUse = None
        self.mongoDBUnansweredQuestionConnector = MongoDBUnansweredQuestionConnector()
        self.corpus = Corpus(self.mongoDBUnansweredQuestionConnector, basePath +"/dictionaries/dictionary")
        self.model = Word2VecModel(self.corpus, basePath +"/savedModels/glove_vector_300")
        # self.model = TFIDFModel(self.corpus, "./savedModels/tfidf.tfidf")
        self.model.initializeModel()
        self.documentRetriever = DocumentIndexRetriever(self.corpus, self.model, basePath +"/indexes/unansweredQuestion.index")
        self.documentRetriever.update()
        self.confidenceThreshold = 0.7
       # self.documentRetriever= DocumentRetrieverByVector(self.corpus, self.wordToVecModel)
     
    def update(self):
        self.documentRetriever.update()
        #maybe train the model here

    def answerQuestion(self,question) -> List[str]:
        answers, confidences = self.documentRetriever.findSimilarDocuments(query=question)
        answersToReturn = []
        for answer, confidence in zip(answers, confidences):
            print("CONFIDENCE")
            print(confidence)
            if confidence >=self.confidenceThreshold:
                answersToReturn.append(answer)
        
        return answersToReturn
   




