from gensim import models

from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.DocumentIndexRetriever import DocumentIndexRetriever
from UnansweredQuestions.Model import Model
import os.path
from os import path

class TFIDFModel(Model):
    def __init__(self, corpus : Corpus, modelPath : str):
        super().__init__(corpus= corpus, modelPath = modelPath)
       


    def _train(self, documents, update = False):
       pass
        
        
    def _fit(self, documents):
        # for doc in documents:
        #     print(doc)

        corpusBow = [self.corpus.convertDocToBow(doc) for doc in documents]
        result = []
        
        for bow in corpusBow:
            transformVector = self.model[bow]
            result.append(transformVector)
        return result

    def getNumFeatures(self):
        return len(self.corpus.dictionary)
    
    def initializeModel(self):
        print("INTIAlIzING MODEL")
        corpusBow = [self.corpus.convertDocToBow(doc) for doc in self.corpus] 
        self.model = models.TfidfModel(corpusBow)  
        
        self.trained = True

    def loadModel(self):
        pass 

    def saveModel(self):
        pass


    # def saveModel(path):
    #     pass
    
    # def loadModel(path):