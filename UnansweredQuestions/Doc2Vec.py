from gensim import models
import gensim.downloader
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from Corpus import Corpus
from Model import Model

class Doc2VecModel(Model):
    def __init__(self, corpus, vector_size, modelPath : str):
        super().__init__(corpus, modelPath)
        self.vector_size = vector_size

    def train(self, corpus : Corpus):
        index = 0
        documents = []
        for doc in corpus: 
            document = TaggedDocument(doc, [index])
            documents.append(document)

            index = index+1

        model = Doc2Vec( vector_size=self.vector_size, window=2, min_count=1, workers=4)
        model.build_vocab(documents)
        model.train(documents, epochs=100, total_examples=model.corpus_count)

        self.model =model
        
    def fit(self, corpus : Corpus):
        vectors = [self.model.infer_vector(doc) for doc in corpus]
        # print(vectors)
        return vectors

    def getNumFeatures(self):
        return self.vector_size

    def loadModel(self):
        self.model = Doc2Vec.load(self.modelPath)


    # def saveModel(path):
    #     pass
    
   