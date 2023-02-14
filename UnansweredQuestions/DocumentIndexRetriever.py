
from gensim import similarities

from UnansweredQuestions.Corpus import Corpus
from UnansweredQuestions.DocumentRetriever import DocumentRetriever
from UnansweredQuestions.Model import Model
from os import path
import numpy as np

class DocumentIndexRetriever(DocumentRetriever):
    def __init__(self, corpus, model : Model, indexPath, topN = 1):
        super().__init__(corpus = corpus, model = model)
        # self.index = None
        self.indexPath = indexPath
        self.topN = topN
        self.index = None
        # if path.exists(self.indexPath):
        #     self.index = self.loadIndex(self.indexPath)
        # else:
        #     self.index = self.createAndSaveIndex()


    def findSimilarDocuments(self,query):
        # index = self.loadIndex(self.indexPath)
        # # bowVectors = self.corpus.convertDocToBow(processedAndTokenizedQuery)
        query = self.corpus.preprocessDoc(query)
       
        transformedVectors = self.model.fitOnDocuments([query])
        # print(transformedVectors)
        if len(transformedVectors) == 0 or len(transformedVectors[0]) ==0:
            print("RETURN")
            return ([], [])

        # try:
        documentSimilarities = self.index[transformedVectors[0]] 
        for i, sim in enumerate(documentSimilarities):  
            doc = self.corpus.getDocumentByIndex(i)
            print(doc)
            print(sim)
    
        return self.getTopDocs(documentSimilarities, self.topN)
        # except:
        #     return ([],[])
     
       
    
    def addNewDocuments(self,documents):
        self.corpus.addDocuments(documents)
        #Recreate the index
        self.createAndSaveIndex(self.indexPath)

    def update(self):
        self.createAndSaveIndex()

    
    def createAndSaveIndex(self):
        # print(self.corpus)
        #self.model.train(self.corpus)
        transformedCorpus = self.model.fitOnDocuments(self.corpus)
        self.index = similarities.Similarity(output_prefix=None, corpus = transformedCorpus, num_features= self.model.getNumFeatures())
        # print(transformedCorpus)
        self.saveIndex(self.indexPath, self.index)



    def saveIndex(self, path, index):
        index.save(path)
    
    def loadIndex(self,path):
        index = similarities.Similarity.load(path)
        return index
    
    #lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2) -- Model is created with something like this
    #index = similarities.MatrixSimilarity(lsi[corpus])  -- Index is created in something like this

