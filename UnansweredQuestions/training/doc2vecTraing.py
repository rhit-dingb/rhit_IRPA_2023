import sys
sys.path.append('../')
from gensim.downloader import info
from gensim import corpora
import gensim.downloader
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from Corpus import Corpus
import os

# print(info()["corpora"].keys())
# print(info()["corpora"]["20-newsgroups"])
# print(info()["corpora"]["text8"])
documents = gensim.downloader.load("20-newsgroups")
# for doc in documents:
#     print(doc)

corpus = Corpus(None, None)

docs= [TaggedDocument(corpus.preprocessDoc(doc["data"]), [i]) for i, doc in enumerate(documents)]
model = Doc2Vec(vector_size=50, min_count=1)
model.build_vocab(docs, update= False)
model.train(docs, epochs=50, total_examples=len(docs))
model.save("../savedModels/doc2vec")
print(os.listdir("../"))