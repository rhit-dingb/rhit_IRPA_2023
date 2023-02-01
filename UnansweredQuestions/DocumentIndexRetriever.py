
from gensim import similarities

from Corpus import Corpus
from DocumentRetriever import DocumentRetriever
from Model import Model
class DocumentIndexRetriever(DocumentRetriever):
    def __init__(self, corpus, model : Model, indexPath, topN = 3):
        super().__init__(corpus = corpus, model = model)
        # self.index = None
        self.indexPath = indexPath
        self.topN = topN


    def findSimilarDocuments(self,query):
        index = self.loadIndex(self.indexPath)
        # # bowVectors = self.corpus.convertDocToBow(processedAndTokenizedQuery)
        query = self.corpus.preprocessDoc(query)
        # print("QUERY!!")
        # print(query)
        # print(query)
        transformedVectors = self.model.fitOnDocuments([query])
        if len(transformedVectors) == 0:
            return []

        documentSimilarities = index[transformedVectors[0]] 
        # print(documentSimilarities)
        return self.getTopDocs(documentSimilarities, self.topN)
        # counter = 0
        # for doc_position, doc_score in sims:
        #     print(doc_score, self.corpus.getDocumentByIndex(doc_position))
        # return documentSimilarities
       
        


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
        index = similarities.Similarity(output_prefix=None, corpus = transformedCorpus, num_features= self.model.getNumFeatures())
        self.saveIndex(self.indexPath, index)



    def saveIndex(self, path, index):
        index.save(path)
    
    def loadIndex(self,path):
        index = similarities.Similarity.load(path)
        return index
    
    #lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2) -- Model is created with something like this
    #index = similarities.MatrixSimilarity(lsi[corpus])  -- Index is created in something like this

