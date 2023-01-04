from gensim import models

from Corpus import Corpus
from DocumentIndexRetriever import DocumentIndexRetriever
from Model import Model

class TFIDFModel(Model):
    def __init__(self, corpus : Corpus, modelPath : str):
        super().__init__(corpus= corpus, modelPath = modelPath)

    def train(self, documents):
        corpusBow = [self.corpus.convertDocToBow(doc) for doc in documents]
        self.model = models.TfidfModel(corpusBow)  
        
        
    def fit(self, documents):
        corpusBow = [self.corpus.convertDocToBow(doc) for doc in documents]
        result = []
        for bow in corpusBow:
            transformVector = self.model[bow]
            result.append(transformVector)
        return result

    def getNumFeatures(self):
        return len(self.corpus.dictionary)
    
    def loadModel(self):
        raise Exception("This model has no save method")

  


    # def saveModel(path):
    #     pass
    
    # def loadModel(path):