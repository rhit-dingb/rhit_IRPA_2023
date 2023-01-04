from collections import defaultdict
from gensim import corpora
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
from gensim import models
from gensim import similarities

from Corpus import Corpus
from Doc2Vec import Doc2VecModel
from DocumentIndexRetriever import DocumentIndexRetriever
from TFIDFModel import TFIDFModel
from Word2Vec import Word2VecModel
# class DocumentRetriever:
#     def __init__(self):
#         self.documents = [
#             "Travis Zheng attends Rose-Hulman institute of technology",
#             "Travis Zheng  is currently 21 years old, and lives in California",
#             "Travis is currently working on a senior project with his teammates, Yiqi, Bowen and Justin",
#             # "Human machine interface for lab abc computer applications",
#             # "A survey of user opinion of computer system response time",
#             # "The EPS user interface management system",
#             # "System and human system engineering testing of EPS",
#             # "Relation of user perceived response time to error measurement",
#             # "The generation of random binary unordered trees",
#             # "The intersection graph of paths in trees",
#             # "Graph minors IV Widths of trees and well quasi ordering",
#             # "Graph minors A survey",
#         ]
#         self.dictionary = None
#         self.model = None
#         self.index = None

#         processedDocs = self.preprocessDocuments(self.documents)
#         self.createModel(processedDocs)

        
#     def preprocessDocuments(self,documents):
#         processedDocuments = []
#         for doc in documents:
#             processDoc = self.preprocessDoc(doc)
#             processedDocuments.append(processDoc)
#         # print(processedDocuments)
#         return processedDocuments


#     def preprocessDoc(self,doc): 
#         processDocument = remove_stopwords(doc)
#         processDocument = preprocess_string(processDocument)
#         return processDocument

#     def query(self,question):
#         processedQuery = self.preprocessDoc(question)
#         vec_bow = self.dictionary.doc2bow(processedQuery)
        
#         vec_model = self.model[vec_bow]  # convert the query to LSI space
#         sims = self.index[vec_model]
#         sims = sorted(enumerate(sims), key=lambda item: -item[1])
#         for doc_position, doc_score in sims:
#             print(doc_score, self.documents[doc_position])


#     #Text is a 2d array, each array has token of a document
#     def createModel(self, texts): 
#         dictionary = corpora.Dictionary(texts)
#         corpus = [dictionary.doc2bow(text) for text in texts]
#         tfidf = models.TfidfModel(corpus)
#         self.model = tfidf
#         self.dictionary = dictionary
#         # Might wanna change this to be more memory efficient
#         # Also note, tfidf[corpus] means convert the bag of words vectors for the corpus to tfidf
#         #[] operator on gensim model means that can be used to convert any vector from the old representation to the new representation
#         self.index = similarities.MatrixSimilarity(tfidf[corpus])


corpus = Corpus()
model = TFIDFModel(corpus, "tfidf.tfidf")
model2 = Doc2VecModel(corpus, 50, "tfidf.tfidf")


print(len(corpus.dictionary))
documentIndexManager = DocumentIndexRetriever(corpus, model2, "unansweredQuestion.index")
documentIndexManager.createAndSaveIndex()

# model2.saveModel()
# model2.loadModel()

# for doc in corpus:
#     print(doc)

# corpus.saveDictionary(corpus.dictionaryPath)


sims = documentIndexManager.findSimilarDocuments("How old is Travis Zheng?")
print(sims)

