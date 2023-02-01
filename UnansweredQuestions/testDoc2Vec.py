from gensim.models.doc2vec import Doc2Vec
from gensim.similarities import Similarity
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim import corpora

from Corpus import Corpus
# Start with a list of documents
documents = Corpus(None)

# Train a Doc2Vec model on the documents

docs= [TaggedDocument(doc, [i]) for i, doc in enumerate(documents)]
model = Doc2Vec(vector_size=50, min_count=1, epochs=40)
print(docs)

dictionary = corpora.Dictionary(documents, "./dictionaries/dictionaryDoc2VecTesting")

model.build_vocab(docs)

model.train(docs, epochs=100, total_examples=model.corpus_count)

# Create vector representations for each document
vectors = [model.infer_vector(doc) for doc in documents]

# Create a similarity index from the vectors
index = Similarity(None, vectors, 50)

# Define a query document
query = ['on','travis', 'zheng','team']


# Convert the query to a vector representation
query_vec = model.infer_vector(query)


# Perform the similarity query
similarity_scores = index[query_vec]

# Print the similarity scores for each document in the corpus
print(similarity_scores)