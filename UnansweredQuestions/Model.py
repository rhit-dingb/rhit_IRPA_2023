from gensim import models

from Corpus import Corpus
from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, corpus : Corpus, modelPath : str):
        self.model = None
        self.corpus : Corpus = corpus
        self.modelPath = modelPath

    @abstractmethod
    def train(self, documents):
       pass

    @abstractmethod  
    def fit(self, documents):
        pass

    @abstractmethod
    def getNumFeatures(self):
       pass

    
    @abstractmethod
    def loadModel(self):
        pass

    def saveModel(self):
        self.model.save(self.modelPath)

   
        

 