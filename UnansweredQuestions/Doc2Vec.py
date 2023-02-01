from gensim import models
import gensim.downloader
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from Corpus import Corpus
from Model import Model

class Doc2VecModel(Model):
    def __init__(self, corpus, vector_size, modelPath : str):
        super().__init__(corpus, modelPath)
        self.vector_size = vector_size

    
    def initializeModel(self):
        self.model = Doc2Vec(vector_size=self.vector_size, window=2, min_count=1, workers=4)
       

    def _train(self, documents, update = False):
        index = 0
        taggedDocuments = []
        for doc in documents: 
            document = TaggedDocument(doc, [index])
            taggedDocuments.append(document)
            index = index+1

        # model = Doc2Vec( vector_size=self.vector_size, window=2, min_count=1, workers=4)

        self.model.build_vocab(taggedDocuments, update= update)
        self.model.train(taggedDocuments, epochs=50, total_examples=len(taggedDocuments))
        self.saveModel()
        
    def _fit(self, documents):
        vectors = [self.model.infer_vector(doc) for doc in documents]
        # print(vectors)
        return vectors

    def getNumFeatures(self):
        return self.vector_size

    def loadModel(self):
        self.model = Doc2Vec.load(self.modelPath)

   