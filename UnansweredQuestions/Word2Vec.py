from gensim import models
import gensim.downloader
from gensim.models import Word2Vec

from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.Model import Model
from gensim.models import KeyedVectors
import gensim.downloader
import numpy as np
class Word2VecModel(Model):
    def __init__(self, corpus : Corpus, modelPath : str):

        super().__init__(corpus= corpus, modelPath = modelPath)
        
    def initializeModel(self):
        pass

    def _train(self, documents, update):
        # glove_vectors = gensim.downloader.load('glove-twitter-25')
        # self.model = glove_vectors()
        # self.model = Word2Vec(["DOCUMENT"], vector_size=100, window=5, min_count=1, workers=4)
        model = Word2Vec( min_count=1, window=5)
        model.build_vocab([list(self.model.index_to_key)])
        model.wv.vectors = self.model.vectors
        model.train(documents, total_examples=len(documents), epochs=10)
        self.saveModel(self.modelPath)
        self.model = model 

    def getNumFeatures(self):
        return len(self.model["test"])

    def _fit(self, corpus):
        vectors = []
        for doc in corpus:
            if doc =="":
                continue
            
            newDoc = []
            for word in doc:
                if not word in self.model.index_to_key:
                    continue
                newDoc.append(word)
            if len(newDoc) == 0:
                continue
            mean = np.mean(self.model[newDoc], axis=0)
            #Normalize the average representation of the document
            mean = mean / np.linalg.norm(mean)
            vectors.append(mean)
        return vectors
                
       

    def saveModel(path):
        # might have to implement this part
        pass
    
    def loadModel(self):
        # print("LOADING", self.modelPath+self.pathExtension)
        self.model = KeyedVectors.load(self.modelPath)
    
