

from gensim import corpora
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
from gensim.utils import simple_preprocess
from UnansweredQuestions.UnasweredQuestionDBConnector import UnansweredQuestionDbConnector
from UnansweredQuestions.constants import DB_UNANSWERED_QUESTION_ANSWER_FIELD_KEY 
import nltk
from nltk.stem import WordNetLemmatizer 


class Corpus:
    def __init__(self, dataSourceConnector : UnansweredQuestionDbConnector, dictionaryPath):
        # self.documents = [
        #     "He is currently 21 years old, and lives in California",
        #     "Travis is currently working on a senior project with his teammates, Yiqi, Bowen and Justin",
        #     "Human machine interface for lab abc computer applications",
        #     "A survey of user opinion of computer system response time",
        #     "The EPS user interface management system",
        #     "System and human system engineering testing of EPS",
        #     "Relation of user perceived response time to error measurement",
        #     "The generation of random binary unordered trees",
        #     "The intersection graph of paths in trees",
        #     "Graph minors IV Widths of trees and well quasi ordering",
        #     "Graph minors A survey",
        #     "A bee is a pollinating animal",
        # ]

        # processedDoc = self.preprocessDocuments(self.documents)
        self.dictionaryPath = dictionaryPath
        self.dataSourceConnector = dataSourceConnector
        self.dictionary = None
        self.lemmatizer = WordNetLemmatizer()
        self.constructDictionary()
      
        # self.documents = self.dataSourceConnector.getAnsweredQuestionSortedByDate()
        # print("DATA", list(self.documents))


    def update(self):
        self.constructDictionary()
        self.saveDictionary(self.dictionaryPath)

    def constructDictionary(self):
       self.dictionary = corpora.Dictionary(doc for doc in self)


    # MAYBE MAKE AN DB CALL HERE
    def __len__(self):
        return len(self.documents)

    def preprocessDoc(self,doc): 
        # processDocument = remove_stopwords(doc)
        processDocument = doc
       
        # processDocument = preprocess_string(processDocument)
        
        processDocument = simple_preprocess(processDocument)
        res = []
        for token in processDocument:
           tokenLemma = self.lemmatizer.lemmatize(token)
           res.append(tokenLemma)
   
        return res

    def preprocessDocuments(self,documents):
        processedDocuments = []
        for doc in documents:
            processDoc = self.preprocessDoc(doc)
            processedDocuments.append(processDoc)
        return processedDocuments   


    def addDocuments(self,documents):
        preprocessedDocuments = self.preprocessDocuments(documents)
        # Add document to database---currently add to list, but probably will replace this with call to database.
        self.documents = self.documents + documents
        self.updateDictionary(preprocessedDocuments)

    # #Probably replace this with database call.
    def getDocumentByIndex(self, doc_position):
        index = 0
        for doc in self.retrieveDocumentFromDataSource():
            if index == doc_position:
                return doc
            index = index +1

    def retrieveDocumentFromDataSource(self):
        # Probably replace this with a database call.
        cursor = self.dataSourceConnector.getAnsweredQuestionSortedByDate()
        for doc in cursor:
            yield doc[DB_UNANSWERED_QUESTION_ANSWER_FIELD_KEY]

        
    def updateDictionary(self,documents):
        self.dictionary.add_documents(documents)

    
    def loadDictionary(self,path):
        self.dictionary = corpora.Dictionary.load(path)

    def saveDictionary(self, path):
        self.dictionary.save(path)
    
    def __iter__(self):
        index = 0
       
        for doc in self.retrieveDocumentFromDataSource():
            # print("DOC")
            # print(doc)
            # yield self.convertDocToBow(doc)
            preprocessDoc = self.preprocessDoc(doc)
            index = index + 1
            yield preprocessDoc

    def convertDocToBow(self,doc):
        return self.dictionary.doc2bow(doc)