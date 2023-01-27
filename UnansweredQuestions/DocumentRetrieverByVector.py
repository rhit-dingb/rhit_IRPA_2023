
from gensim import similarities

from Corpus import Corpus
from DocumentRetriever import DocumentRetriever
from Model import Model
from sklearn.metrics.pairwise import cosine_similarity

class DocumentRetrieverByVector(DocumentRetriever):
    def __init__(self, corpus, model : Model, topN = 3):
        super().__init__(corpus = corpus, model = model)
        self.topN = topN
        # self.index = None
        # self.indexPath = indexPath


    def findSimilarDocuments(self,query):
        query = self.corpus.preprocessDoc(query)
        # print("QUERY!!")
        # print(query)
        # print(query)
        transformedVectors = self.model.fitOnDocuments([query])
        # print(transformedVectors)
        documentVectors = []
        documentVectors = self.model.fitOnDocuments(self.corpus)
        # for doc in self.corpus:
        #     fittedDoc = self.model.fit([doc])
        #     documentVectors.append(fittedDoc[0])
        
        transformedVector = transformedVectors[0]
        # print(transformedVector)
        # print(documentVectors)

        documentSimilarities = []
        for vector in documentVectors:
            # print(vector)
            sim = cosine_similarity([transformedVector], [vector])
            documentSimilarities.append(sim[0])

        
        return self.getTopDocs(documentSimilarities, self.topN)

        # sims = sorted(sims, key=lambda item: -item[0])
        # for sim in sims:
        #     print(sim)
        #     print(self.corpus.getDocumentByIndex(index))
        #     index = index + 1


        # print(documentSimilarities)
        # sims = sorted(enumerate(documentSimilarities), key=lambda item: -item[1])

        # for doc_position, doc_score in sims:
        #     print(doc_score, self.corpus.getDocumentByIndex(doc_position))
        # return documentSimilarities
    

    def addNewDocuments(self,documents):
        self.corpus.addDocuments(documents)
        #Recreate the index
        # self.createAndSaveIndex(self.indexPath)

    def update(self):
        pass

    

    #lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2) -- Model is created with something like this
    #index = similarities.MatrixSimilarity(lsi[corpus])  -- Index is created in something like this

