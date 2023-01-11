from typing import List, Tuple
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
    def addNewDocuments(self,documents):
        pass

    @abstractmethod
    def update(self):
        pass


    def getTopDocs(self,documentSimilarities : List[int], topN):
        counter = 0
        topDocs = []
        similarityWithIndex = sorted(enumerate(documentSimilarities), key=lambda item: -item[1])
        for doc_position, doc_score in similarityWithIndex:
            if counter == topN:
                return topDocs
            
            document = self.corpus.getDocumentByIndex(doc_position)
            topDocs.append(document)
            counter = counter + 1
            # print(doc_score, self.corpus.getDocumentByIndex(doc_position))


 