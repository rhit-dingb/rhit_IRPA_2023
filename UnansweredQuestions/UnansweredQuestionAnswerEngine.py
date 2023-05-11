



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
from UnansweredQuestions.SentenceEmbeddingModel import SentenceEmbeddingModel


import sys
import os
import nltk

try:
    nltk.find('corpora/wordnet')
except Exception:
    nltk.download('wordnet')

try:
    nltk.find('omw-1.4')
except Exception:
    nltk.download('omw-1.4')


class UnansweredQuestionAnswerEngine:
    """
    This class is handles providing answer to addressed unanswered questions by using models that can be swapped out.
    """
    # Basepath: ./UnansweredQuestions, or ../UnansweredQuestions
    def __init__(self, databaseConnector : UnansweredQuestionDbConnector):
        self.modelToUse = None
        self.dbConnector = databaseConnector
        basePath = self.determinePath()
       

      
        self.dictionaryDir = os.path.join(basePath, "dictionaries")
        self.dictionaryPath = os.path.join(basePath, self.dictionaryDir, "dictionary")
       

        self.modelDir = os.path.join(basePath, "savedModels")
        self.modelPath = os.path.join(basePath, self.modelDir, "wordVectorModel")

        self.indexDir = os.path.join(basePath, "indexes")
        self.indexPath =  os.path.join(basePath, "unansweredQuestion.index")
        self.makeDirectory()
        
        self.corpus = Corpus(self.dbConnector, self.dictionaryPath)
        self.model : Model = Word2VecModel(self.corpus, self.modelPath )
        #self.model = SentenceEmbeddingModel(corpus = self.corpus)
        # self.model.initializeModel()
        self.documentRetriever = DocumentIndexRetriever(self.corpus, self.model, self.indexPath)
        self.update()
       
     
    def makeDirectory(self):
        if not os.path.exists(self.modelDir):
            os.makedirs(self.modelDir)

        if not os.path.exists(self.dictionaryDir):
            os.makedirs(self.dictionaryDir)

        if not os.path.exists(self.indexDir):
            os.makedirs(self.indexDir)


    def determinePath(self):
        # base_dir = os.path.relpath()
        # unansweredQues_dir = os.path.join(base_dir, "UnansweredQuestions")
        # print(unansweredQues_dir)
        # return unansweredQues_dir 
        return os.path.dirname(os.path.abspath(__file__))
        

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
            if confidence >=self.model.scoreThreshold:
                answersToReturn.append(answer)
        
        return answersToReturn
   
   




