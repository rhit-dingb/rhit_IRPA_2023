from gensim import models
import gensim.downloader
from gensim.models import Word2Vec

from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.Model import Model
from gensim.models import KeyedVectors
import gensim.downloader
import numpy as np
import os
import tensorflow_hub as hub
import tensorflow as tf
class SentenceEmbeddingModel(Model):
    def __init__(self, corpus : Corpus):
        self.module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        super().__init__(corpus= corpus, modelPath = None, threshold=0.6)
       

    def initializeModel(self):
        self.model  = hub.load(self.module_url)

    def _train(self, documents, update):
        return 

    def getNumFeatures(self):
        return 512

    def _fit(self, corpus):
        embeddings = []
        for document in corpus:
            documentString = " ".join(document)
            # print(documentString)
            embedding : tf.Tensor  = self.model([documentString])
            # print(embedding[0].numpy())
            # print(embedding[0])
           
            embeddings.append(embedding[0].numpy())

        return embeddings
                
       
    def saveModel(self):
        # might have to implement this part
        pass
    
    def loadModel(self):
        # print("LOADING", self.modelPath+self.pathExtension)
        pass
