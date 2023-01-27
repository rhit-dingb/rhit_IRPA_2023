

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
from gensim.scripts.glove2word2vec import glove2word2vec
import gensim.downloader
from gensim.test.utils import datapath, get_tmpfile
import time
from gensim.downloader import info


print(info()["corpora"].keys())

corpus = Corpus(None, "./dictionaries/dictionary")
# model = gensim.downloader.load("doc2vec-wikipedia-dbow")

# glove_vectors = gensim.downloader.load('glove-wiki-gigaword-300')
# glove_vectors.save("./savedModels/glove_vector_300.bin"

# glove_file = datapath('./savedModels/glove_vector_300.txt')
# tmp_file = get_tmpfile("./savedModels/test_word2vec.txt")


# # glove2word2vec("./savedModels/glove_vector_300.txt", tmp_file)
# wordToVecModel = Word2VecModel(corpus, "./savedModels/glove_vector_300.bin")
# wordToVecModel.trainModel(corpus, True)

# # model = TFIDFModel(corpus, "./savedModels/tfidf.tfidf")
# # model.trainModel(corpus)


model2 = Doc2VecModel(corpus, 50, "./savedModels/Doc2Vec")

# documentIndexManager = DocumentIndexRetriever(corpus, model2, "./indexes/unansweredQuestion.index")
# documentIndexManager.createAndSaveIndex()

# # model2.loadModel()
# model2.initializeModel()
model2.trainModel(corpus, True)

# documentIndexManager = DocumentIndexRetriever(corpus, wordToVecModel, "./indexes/unansweredQuestion.index")
# documentIndexManager.createAndSaveIndex()

# start = time.time()
# sims = documentIndexManager.findSimilarDocuments("What age is Travis Zheng?")
# print(sims)
# end = time.time()
# print(end-start)

# # #Should be faster
# start = time.time()
# sims = documentIndexManager.findSimilarDocuments("What is a glacier made of?")
# print(sims)
# end = time.time()
# print(end-start)

documentRetrieverByVector = DocumentRetrieverByVector(corpus, model2)
start = time.time()
docs = documentRetrieverByVector.findSimilarDocuments("What age is travis zheng")
print(docs)
end = time.time()
print(end-start)

# start = time.time()
# docs = documentRetrieverByVector.findSimilarDocuments("What is a seismograph?")
# print(docs)
# end = time.time()
# print(start - end)


# model2.saveModel()
# model2.loadModel()

# for doc in corpus:
#     print(doc)

# corpus.saveDictionary(corpus.dictionaryPath)


