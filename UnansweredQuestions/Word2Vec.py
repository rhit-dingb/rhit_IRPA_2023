from gensim import models
import gensim.downloader
from gensim.models import Word2Vec

from Corpus import Corpus

class Word2VecModel:
    def __init__(self):
        self.model = None

    def train(self, corpus : Corpus):
        # glove_vectors = gensim.downloader.load('glove-twitter-25')
        # self.model = glove_vectors()
        self.model = Word2Vec(["DOCUMENT"], vector_size=100, window=5, min_count=1, workers=4)
        
    def fit(self, corpus):
        return self.model[corpus]

    # def saveModel(path):
    #     pass
    
    # def loadModel(path):