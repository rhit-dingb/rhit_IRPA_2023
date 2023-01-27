from gensim import models
import gensim.downloader
from gensim.models import Word2Vec

from Corpus import Corpus
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
        pass

    def getNumFeatures(self):
        return len(self.model["test"])

    def _fit(self, corpus):
        # print(self.model)
        # print(corpus)
        # print([self.model[doc] for doc in corpus])
        vectors = []
        for doc in corpus:
            newDoc = []
            for word in doc:
                if not word in self.model.index_to_key:
                    continue
                newDoc.append(word)
            mean = np.mean(self.model[newDoc], axis=0)
            vectors.append(mean)
        return vectors
                
        #    similar_words = self.model.most_similar(positive=[word],topn=1)

    def saveModel(path):
        pass
    
    def loadModel(self):
        self.model = KeyedVectors.load(self.modelPath)
        # print("LOADED MODEL")
        # print(self.model)


        # ss= self.model[["fuck", "you"]]
        # print(ss)
        # self.model  = gensim.downloader.load('glove-wiki-gigaword-300')