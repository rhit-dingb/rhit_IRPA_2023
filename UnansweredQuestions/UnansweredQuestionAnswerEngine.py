



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
   #self.model = TFIDFModel(self.corpus, "./savedModels/tfidf.tfidf")

class UnansweredQuestionAnswerEngine:
    # Basepath: ./UnansweredQuestions, or ../UnansweredQuestions
    def __init__(self):
        self.modelToUse = None
        self.mongoDBUnansweredQuestionConnector = MongoDBUnansweredQuestionConnector(self)
        basePath = self.determinePath()
        self.corpus = Corpus(self.mongoDBUnansweredQuestionConnector, basePath +"/dictionaries/dictionary")
        self.model = Word2VecModel(self.corpus, basePath +"/savedModels/glove_vector_300")
     
        self.model.initializeModel()
        self.documentRetriever = DocumentIndexRetriever(self.corpus, self.model, basePath +"/indexes/unansweredQuestion.index")
        self.documentRetriever.update()
        self.confidenceThreshold = 0.8
       # self.documentRetriever= DocumentRetrieverByVector(self.corpus, self.wordToVecModel)
    def determinePath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        unansweredQues_dir = os.path.join(base_dir, "UnansweredQuestions")
        return unansweredQues_dir 

    def update(self):
        self.corpus.update()
        self.documentRetriever.update()
        print("UPDATED")
        #maybe train the model here

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
   




