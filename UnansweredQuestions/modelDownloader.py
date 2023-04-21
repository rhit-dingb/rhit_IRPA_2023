

import sys
import os
from gensim import corpora
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
from gensim import models
from gensim import similarities

sys.path.append('../')

from DocumentRetrieverByVector import DocumentRetrieverByVector
from MongoDBUnansweredQuestionConnector import MongoDBUnansweredQuestionConnector
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

glove_vectors = gensim.downloader.load('glove-wiki-gigaword-300')
glove_vectors.save("./savedModels/glove_vector_300")



