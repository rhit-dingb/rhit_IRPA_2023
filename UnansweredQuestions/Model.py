from gensim import models

from Corpus import Corpus
from abc import ABC, abstractmethod
import os.path
from os import path


class Model(ABC):
    def __init__(self, corpus : Corpus, modelPath : str ):
        self.model = None
        self.corpus : Corpus = corpus
        self.modelPath = modelPath
        self.trained = False
        if self.model is None and path.exists(self.modelPath):
            self.model = self.loadModel()
            self.trained = True
        else:
            self.initializeModel()


    # This method should only instantiate the untrained model, but not save it. We should only save a model when it is trained
    @abstractmethod
    def initializeModel(self):
        pass


    def trainModel(self, documents, update = False):
        self._train(documents, update)
        self.trained = True

    @abstractmethod
    def _train(self, documents, update = False):
       pass

 
    def fitOnDocuments(self, documents):
        if self.trained:
            return self._fit(documents)
        else:
            return []

    @abstractmethod  
    def _fit(self, documents):
        pass

    @abstractmethod
    def getNumFeatures(self):
       pass

    
    @abstractmethod
    def loadModel(self):
        pass

    def saveModel(self):
        self.model.save(self.modelPath)


   
        

 