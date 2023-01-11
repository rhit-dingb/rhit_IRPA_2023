from gensim import models

from Corpus import Corpus
from DocumentIndexRetriever import DocumentIndexRetriever
from Model import Model
import os.path
from os import path

class TFIDFModel(Model):
    def __init__(self, corpus : Corpus, modelPath : str):
        super().__init__(corpus= corpus, modelPath = modelPath)


    def _train(self, documents, update = False):
        corpusBow = [self.corpus.convertDocToBow(doc) for doc in documents]
        self.model = models.TfidfModel(corpusBow)  
        
        
    def _fit(self, documents):
        corpusBow = [self.corpus.convertDocToBow(doc) for doc in documents]
        result = []
        for bow in corpusBow:
            transformVector = self.model[bow]
            result.append(transformVector)
        return result

    def getNumFeatures(self):
        return len(self.corpus.dictionary)
    
    def initializeModel(self):
        pass

    def loadModel(self):
        pass 

    def saveModel(self):
        pass


    # def saveModel(path):
    #     pass
    
    # def loadModel(path):