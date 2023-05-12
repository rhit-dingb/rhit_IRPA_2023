
from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.DocumentRetriever import DocumentRetriever
from UnansweredQuestions.Model import Model
from sklearn.metrics.pairwise import cosine_similarity

class DocumentRetrieverByVector(DocumentRetriever):
    def __init__(self, corpus, model : Model, topN = 3):
        super().__init__(corpus = corpus, model = model)
        self.topN = topN
        # self.index = None
        # self.indexPath = indexPath


    def findSimilarDocuments(self,query):
        # query = self.corpus.preprocessDoc(query)
     
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
            # print(sim)
            documentSimilarities.append(sim[0])

        
        return self.getTopDocs(documentSimilarities, self.topN)

    

    def update(self):
        pass

    
