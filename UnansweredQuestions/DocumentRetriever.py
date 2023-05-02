from typing import List, Tuple
from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.Model import Model
from abc import ABC, abstractmethod
import numpy as np

class DocumentRetriever(ABC):
    """
    Abstract class for document retriever that uses a given model to retrieve top n document from the corpus.
    """
    def __init__(self, corpus : Corpus, model : Model ):
        self.corpus = corpus
        self.model = model

    @abstractmethod
    def findSimilarDocuments(self,query : str):
        """
        Given a query, find similar documents in the corpus using the model.
        The number of documents return depends on the concrete implementation.
        :param query: question user asked
        """
        pass

    # @abstractmethod
    # def addNewDocuments(self,documents):
    #     pass

    @abstractmethod
    def update(self):
        """
        This function is called when a document is added or deleted from the backend data source so the retriever can react accordingly 
        by updating its index or do nothing
        """
        pass

    
    def getTopDocs(self, documentSimilarities : List[float], topN) ->Tuple[List[int], List[float]]:
        """
        Get the top n similar documents given a list of similarity for each document.
        :param documentSimilarities: A list. The value corresponds to the document similarity to the user query for the document at
        a particular index in the list of documents in the data source.
        """
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


 