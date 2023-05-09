import random
import threading
from typing import Dict, List, Tuple
from Knowledgebase.Knowledgebase import KnowledgeBase
from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline,  FAQPipeline,  Pipeline
from haystack.nodes import FARMReader, RouteDocuments
from haystack import Document, Label, Answer
from DataManager.DataManager import DataManager
import os
from haystack import Document, Label, Answer
from Data_Ingestion.constants import TEMPLATE_LABEL
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel
import Knowledgebase.QuestionAnswerKnowledgebase.utils as utils
from Knowledgebase.QuestionAnswerKnowledgebase.Training.Trainer import Trainer
import pandas as pd

from Knowledgebase.QuestionAnswerKnowledgebase.DocumentStoreConnection import DocumentStoreConnection

class QuestionAnswerKnowledgeBase(KnowledgeBase):
    """
    Concrete implementation of knowledgebase that uses Haystack library to conduct semantic search.
    """
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager

        self.documentStoreConnection = DocumentStoreConnection()
        self.documentStore =  self.documentStoreConnection.determineDocumentStore()
        self.startingReader = "deepset/roberta-base-squad2"
        self.startingRetriever = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
        self.trainedReaderPath = "TrainedModels\QAReader"
        self.trainedRetrieverPath = "TrainedModels\QARetriever"
        self.yearToDocumentStore = dict()
        self.source = "QuestionAnswerKnowledgebase"
        dirname = os.path.dirname(__file__)
        self.fullReaderPath = os.path.join(dirname, self.trainedReaderPath)   
        self.fullRetrieverPath = os.path.join(dirname, self.trainedRetrieverPath)  

        self.retriever = None
        self.reader = None
        self.pipeline = None
        self.scoreThreshold = 0.1
        self.trainer = Trainer()
        self.middleMan =  QuestionToAnswer()
        self.isTraining = False
        self.trainThread : threading.Thread = None
        self.trainingCallback = None


    async def initialize(self):
        """
        This function initializes the knowledgebase by loading the retriever and reader model. If the models do not exist on the local disk, it 
        will download the model and save them to TrainedModels folder.
        """
        if not os.path.exists(self.fullReaderPath):
            os.makedirs(self.fullReaderPath)

        if not os.path.exists(self.fullRetrieverPath):
            os.makedirs(self.fullRetrieverPath)


        dir = os.listdir(self.fullRetrieverPath)
        if len(dir) == 0:
            self.loadRetriever(self.startingRetriever, self.fullRetrieverPath)
        else:
            self.loadRetriever(self.fullRetrieverPath, self.fullRetrieverPath, save=False)

        # dirname = os.path.dirname(__file__)
        # fullPath = os.path.join(dirname, self.trainedModelPath)   
        dir = os.listdir(self.fullReaderPath)
        if len(dir) == 0:
            self.loadReader(self.startingReader, self.fullReaderPath)
        else:
            self.loadReader(self.fullReaderPath, self.fullReaderPath, save=False)

        await self.writeDocToDocumentStore(delete=True)
        # self.pipeline = ExtractiveQAPipeline(self.reader, self.retriever)
        self.pipeline = Pipeline()
        self.pipeline.add_node(component=self.retriever, name="Retriever", inputs=["Query"])
        # route_documents = RouteDocuments()
        # self.pipeline.add_node(component=route_documents, name="RouteDocuments", inputs=["Retriever"])
        self.pipeline.add_node(component=self.middleMan, name="QuestionToAnswer", inputs=["Retriever"])
        
        self.pipeline.add_node(component=self.reader, name="Reader", inputs=["QuestionToAnswer"])


    def loadReader(self, loadPath, pathToSave, save=True):
        self.reader = FARMReader(model_name_or_path=loadPath, use_gpu=True, context_window_size=1000)
        if save:
            self.reader.save(pathToSave)
        self.reader = FARMReader(model_name_or_path=loadPath, use_gpu=True, context_window_size=1000 )
        print("LOADED READER", self.reader)
       
    def loadRetriever(self, loadPath, pathToSave, save=True):
        self.retriever = EmbeddingRetriever(
            embedding_model= loadPath,
            document_store=self.documentStore
        )
        if save:
            self.retriever.save(pathToSave)



    async def writeDocToDocumentStore(self, delete : bool =False ):
        """
        This async function is used during startup initialization to write all uploaded annual and year agnostic data in the database 
        to the document store.

        :param delete: boolean value specifying whether to delete all documents in the document store first before writing.
        :return: none
        """
        if (delete== True):
            self.documentStore.delete_documents()

        availableYears = self.dataManager.getAllAvailableYearsSorted()
        yearAgnosticData = self.dataManager.findAllYearAngosticDataName()

        await self.documentStoreConnection.writeDocToDocumentStore(availableYears, yearAgnosticData,self.dataManager, self.documentStore, self.convertToDf)
        self.documentStore.update_embeddings(self.retriever)
        


    def getAvailableOptions(self, intent, entities, startYear, endYear):
        raise NotImplementedError()

   
    async def searchForAnswer(self, question, intent, entitiesExtracted, startYear, endYear) -> Tuple[List[ChatbotAnswer], bool]:
        result = self.pipeline.run(query = question, params= {
            "Retriever": {"top_k": 15}, 
            "Reader": {"top_k": 5},
            "filters": {
                "$or": {
                    "$and": {
                        "startYear": startYear,
                        "endYear": endYear
                        },

                    "isYearAgnostic": True
                }
            }
             
        })

        # print(result)
        answers : List[Answer] = result["answers"]
        print("THE RESULT")
        for answer in answers:
            print(answer.answer, ":", answer.context, ":", answer.score)
          
        chatbotAnswers : List[ChatbotAnswer]= []
       
        for answer in answers:
            print(answer)
            print(answer.score)
            if answer.score < self.scoreThreshold:
                print("SKIP")
                continue
            
            chatbotAnswer = self.constructAnswer(answer, result)
            print("APPENDING")
            chatbotAnswers.append(chatbotAnswer)

        if len(chatbotAnswers) == 0:
            chatbotAnswers = self.getBackupAnswer(answers, result)

        return (chatbotAnswers, True)
    
    def constructAnswer(self, answer : Answer, result):
        document : Document= utils.findDocumentWithId(answer.document_ids[0], result["documents"])
        metadata=dict()
        metadata["context"] =answer.context
        metadata["offsets_in_document"] = answer.offsets_in_context
        metadata["document_ids"]= answer.document_ids
        metadata["actual answer"] = answer.answer
        metadata["document_content"] = document.content
        metadata["document_question"] = document.meta["query"]
        # print("DOC META")
        # print(document.meta)
        chatbotAnswer = ChatbotAnswer(answer = document.content, source=self.source, metadata= metadata)
        return chatbotAnswer
        # chatbotAnswers.append(chatbotAnswer)
    

    def getBackupAnswer(self, answers : List[Answer], result):
        backupAnswers = []
        for answer in answers:
            chatbotAnswer = self.constructAnswer(answer, result)
            backupAnswers.append(chatbotAnswer)
        return backupAnswers
    

    
    def convertToDf(self,documents : List[Document]):
        """
        Function to convert a list of documents with the answer as content to a 
        dictionary object with the content key as the question instead of the answer so documents can be 
        matched first using the question to user query.
        """
        data = [[doc.meta["query"], doc.content] for doc in documents]
      
        df = pd.DataFrame(data= data, columns=["question", "answer"])
        df.fillna(value="", inplace=True)
        
        df["question"] = df["question"].apply(lambda x: x.strip())
        questions = list(df["question"].values)
        df["embedding"] = self.retriever.embed_queries(queries=questions).tolist()
        df = df.rename(columns={"question": "content"})
        if(len(documents)>0):
        # add rest of metadata
            allMetadata = dict()
            for doc in documents:
                for key in doc.meta:
                    if not key in allMetadata:
                        allMetadata[key] = []
                    allMetadata[key].append(doc.meta[key])
            for key in allMetadata:
                df[key] = allMetadata[key]
            
                  
        #Add id
        ids = [document.id for document in documents]
        df["id"] = ids
        docs_to_index = df.to_dict(orient="records")
        return docs_to_index
    
    

    def train(self, trainingLabels : List[MultiFeedbackLabel], callback):
        if self.isTraining and not self.trainThread == None:
            if self.trainThread.is_alive():
                print("TRAINING THREAD IS ALIVE")
                return False        

        # try:
            # self.trainer.trainDataForEmbeddingRetriever(trainingLabels, self.retriever, saveDirectory=self.fullRetrieverPath,documentStore= self.documentStore, source=self.source, useQuestion=True )
            # self.trainer.trainDataForModelWithSQUAD(trainingLabels=trainingLabels, model=self.reader, saveDirectory= self.fullReaderPath, source=self.source)
        trainingThread = TrainingThread("trainingThread"+str(random.random()), "traingThread", trainingLabels, self.trainer,self)
        trainingThread.start()
        self.trainThread = trainingThread
        self.trainingCallback = callback
        print("TRAINING STARTED")
        return True
        # except Exception:
        #     return False
        
    def doneTraining(self, isSuccess):
        print("TRAINING DONE")
        self.isTraining = False
        self.trainThread = None
        self.documentStore.update_embeddings(self.retriever)
        self.trainingCallback(isSuccess)
        self.trainingCallback = None
      
    
    async def dataUploaded(self, dataName, startYear = None, endYear = None):
        self.documentStore.delete_documents(filters={"dataName": dataName})
        dataDict = {"dataName": dataName}
        if not startYear == None and not endYear == None:
            dataDict["startYear"] = startYear
            dataDict["endYear"] = endYear
        await self.documentStoreConnection.writeDocToDocumentStoreWithDataName([dataDict], self.dataManager, self.documentStore, self.convertToDf )
        self.documentStore.update_embeddings(self.retriever)

    def dataDeleted(self, dataName):
        print("DELETE DOCUMENT")
        self.documentStore.delete_documents(filters={"dataName": dataName})
        print("________")
        print(self.documentStore.get_all_documents(filters={"dataName":dataName}))
        # self.documentStore.update_embeddings(self.retriever)



from haystack.nodes.base import BaseComponent

class QuestionToAnswer(BaseComponent):
    """
    A Haystack node component that will be added after the retriever and before the reader component
    so that the retriever will retrieve documents(qa pairs) based on matching questions and the reader will
    extract answer based on the actual answer itself. This class's run function swaps the content of the document to use the answer 
    instead of the question.

    """
    # If it's not a decision component, there is only one outgoing edge
    outgoing_edges = 1

    def run(self, query: str, documents : List[Document]):
        # Insert code here to manipulate the input and produce an output dictionary
    
        newDocuments = []
        for document in documents:
            newDocument = Document(content= document.meta["answer"], id=document.id, meta = document.meta)
            newDocuments.append(newDocument)
            # print(document.meta)

        output={
            "query":query,
            "documents": newDocuments,
        }

      
        return output, "output_1"

    def run_batch(self, queries: List[str], documents : List[Document]):
        newDocuments = []
        for query in queries:
            output, name = self.run(query=query, documents=documents)
            # print(output)
            docs = output["documents"]
            newDocuments = newDocuments + docs

        output={
            "queries":queries,
            "documents": newDocuments,
        }
           
        return output, "output_1"




class TrainingThread (threading.Thread):
   """
   A training thread class that will created to train the retriever and reader component.
   """
   def __init__(self, threadID, name, trainingLabels : List[MultiFeedbackLabel],trainer : Trainer, knowledgebase : QuestionAnswerKnowledgeBase):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.trainingLabels = trainingLabels
      self.trainer : Trainer = trainer
      self.knowledgebase = knowledgebase

   def run(self):
        try:
            self.trainer.trainDataForEmbeddingRetriever(self.trainingLabels, self.knowledgebase.retriever, saveDirectory=self.knowledgebase.fullRetrieverPath,documentStore= self.knowledgebase.documentStore, source=self.knowledgebase.source, useQuestion=True )
            self.trainer.trainDataForModelWithSQUAD(trainingLabels=self.trainingLabels, model=self.knowledgebase.reader, saveDirectory= self.knowledgebase.fullReaderPath, source=self.knowledgebase.source)
            print("OKAY DONE")
            self.knowledgebase.doneTraining(True)
        except Exception:
            self.knowledgebase.doneTraining(False)
