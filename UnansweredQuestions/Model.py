from gensim import models

from UnansweredQuestions.Corpus import Corpus
from abc import ABC, abstractmethod
import os.path
from os import path


class Model(ABC):
    def __init__(self, corpus : Corpus, modelPath : str):
        self.model = None
        self.corpus : Corpus = corpus
        self.modelPath = modelPath
        self.trained = False
   
        # print(path.exists(self.modelPath))
        if self.model is None and path.exists(self.modelPath):
            self.loadModel()
            self.trained = True
        else:
            print("MODEL NOT FOUND At MODEL PATH, INITIALIZING MODEL..")
            self.initializeModel()


    # This method should only instantiate the untrained model, but not save it. We should only save a model when it is trained
    @abstractmethod
    def initializeModel(self):
        pass


    def trainModel(self, documents, update = False):
        self._train(documents, update)
        self.trained = True

    def fitOnDocuments(self, documents):
        return self._fit(documents)
        # if self.trained:
        #     return self._fit(documents)
        # else:
        #     return []

    @abstractmethod
    def _train(self, documents, update = False):
       pass

 
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


   
        

 