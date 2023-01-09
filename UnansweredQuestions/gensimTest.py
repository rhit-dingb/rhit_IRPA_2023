

import sys

from DocumentRetrieverByVector import DocumentRetrieverByVector
sys.path.append('../')
from gensim import corpora
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
from gensim import models
from gensim import similarities

from Corpus import Corpus
from Doc2Vec import Doc2VecModel
from DocumentIndexRetriever import DocumentIndexRetriever
from TFIDFModel import TFIDFModel
from Word2Vec import Word2VecModel


corpus = Corpus(None, "./dictionaries/dictionary")
model = TFIDFModel(corpus, "./modeles/tfidf.tfidf")
model.trainModel(corpus)


model2 = Doc2VecModel(corpus, 50, "./models/Doc2Vec")
# model2.loadModel()
model2.initializeModel()
model2.trainModel(corpus)

documentIndexManager = DocumentIndexRetriever(corpus, model2, "./indexes/unansweredQuestion.index")
documentIndexManager.createAndSaveIndex()
sims = documentIndexManager.findSimilarDocuments("What age is Travis Zheng?")
print(sims)



# documentRetrieverByVector = DocumentRetrieverByVector(corpus, model2)

# docs = documentRetrieverByVector.findSimilarDocuments("Who is on travis' team?")
# print(docs)
# model2.saveModel()
# model2.loadModel()

# for doc in corpus:
#     print(doc)

# corpus.saveDictionary(corpus.dictionaryPath)


