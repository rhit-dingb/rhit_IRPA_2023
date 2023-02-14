from typing import List, Tuple
from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.Model import Model
from abc import ABC, abstractmethod
import numpy as np

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


    def getTopDocs(self, documentSimilarities : List[int], topN):
        counter = 0
        topDocs = []
        confidence = []
        similarityWithIndex = sorted(enumerate(documentSimilarities), key=lambda item: -item[1])
      
        for doc_position, doc_score in similarityWithIndex:
            if counter == topN:
                return (topDocs, confidence)
            
            document = self.corpus.getAnswerByIndex(doc_position)
            topDocs.append(document) 
            confidence.append(doc_score)
            counter = counter + 1

        if counter> 0:
            return (topDocs, confidence)
        else:
            return ([], [])
            # print(doc_score, self.corpus.getDocumentByIndex(doc_position))


 