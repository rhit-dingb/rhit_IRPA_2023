from typing import Iterable, List
from gensim import models

from UnansweredQuestions.Corpus import Corpus
from abc import ABC, abstractmethod
import os.path
from os import path


class Model(ABC):
    """
    Abstract model class representing a model to convert unanswered questions to number/vector representation.
    """
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

    @abstractmethod
    def initializeModel(self):
        """
        This function is called when no model is found to be saved in the savedModels folder.
        """
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
    def _train(self, documents : Iterable[str], update: bool):
       """
       Train the model given a list of documents. The update flag specifies whether new documents that the model
       has never seen before is given
       This method may not be fully flushed out as no model current trains.

       """
       pass

 
    @abstractmethod  
    def _fit(self, documents : Iterable[str]) -> List[List[float]]:
        """
        This function should convert the list of documents to their vectorized representation based on the model.
        :param documents: A iterable object -- list of strings or the any class that implement the __iter__ function that returns a string on 
        each iteration such as the Corpus class 

        :return: 2D list. For each document, there is a vector representation of that document.
        """
        pass

    @abstractmethod
    def getNumFeatures(self) -> float:
       """
       Get the length of the vector that will be used to represent one document.
       """
       pass

    
    @abstractmethod
    def loadModel(self):
        """
        Load the model.
        """
        pass
    
    @abstractmethod
    def saveModel(self):
        """
        Save the model to disk.
        """
        pass


   
        

 