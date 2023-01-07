from Corpus import Corpus
from Model import Model
from abc import ABC, abstractmethod

class DocumentRetriever(ABC):
    def __init__(self, corpus : Corpus, model : Model ):
        self.corpus = corpus
        self.model = model

    @abstractmethod
    def findSimilarDocuments(self,query):
        pass

    @abstractmethod
    def addNewDocument(self,document):
        pass

    @abstractmethod
    def update(self):
        pass


 