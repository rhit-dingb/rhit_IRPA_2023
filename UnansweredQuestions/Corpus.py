

from gensim import corpora
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string


class Corpus:
    def __init__(self):
        self.documents = [
            "Travis Zheng attends Rose-Hulman institute of technology",
            "He is currently 21 years old, and lives in California",
            "Travis is currently working on a senior project with his teammates, Yiqi, Bowen and Justin",
            "Travis' favorite food is........"
            # "Human machine interface for lab abc computer applications",
            # "A survey of user opinion of computer system response time",
            # "The EPS user interface management system",
            # "System and human system engineering testing of EPS",
            # "Relation of user perceived response time to error measurement",
            # "The generation of random binary unordered trees",
            # "The intersection graph of paths in trees",
            # "Graph minors IV Widths of trees and well quasi ordering",
            # "Graph minors A survey",
        ]
        processedDoc = self.preprocessDocuments(self.documents)
        self.dictionary = corpora.Dictionary(processedDoc)
        self.dictionaryPath = "dictionary"

    def constructDictionary(self):
       self.dictionary = corpora.Dictionary(doc for doc in self)

 

    def preprocessDoc(self,doc): 
        processDocument = remove_stopwords(doc)
        processDocument = preprocess_string(processDocument)
        return processDocument

    def preprocessDocuments(self,documents):
        processedDocuments = []
        for doc in documents:
            processDoc = self.preprocessDoc(doc)
            processedDocuments.append(processDoc)
        # print(processedDocuments)
        return processedDocuments   

    def addDocument(self,document):
        preprocessedDocument = self.preprocessDoc(document)
        # Add document to database---currently add to list, but probably will replace this with call to database.
        self.documents.append(document)
        self.updateDictionary([preprocessedDocument])

    #Probably replace this with database call.
    def getDocumentByIndex(self, doc_position):
        return self.documents[doc_position]

    def retrieveDocumentFromDataSource(self):
        # Probably replace this with a database call.
        for doc in self.documents:
            yield doc

        

    def updateDictionary(self,documents):
        self.dictionary.add_documents(documents)

    
    def loadDictionary(self,path):
        self.dictionary = corpora.Dictionary.load(path)

    def saveDictionary(self, path):
        self.dictionary.save(path)
    
    def __iter__(self):
        for doc in self.retrieveDocumentFromDataSource():
            # yield self.convertDocToBow(doc)
            preprocessDoc = self.preprocessDoc(doc)
            yield preprocessDoc

    def convertDocToBow(self,doc):
        return self.dictionary.doc2bow(doc)