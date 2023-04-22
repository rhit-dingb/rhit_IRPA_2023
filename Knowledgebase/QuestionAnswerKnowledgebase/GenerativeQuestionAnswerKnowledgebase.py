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
from Data_Ingestion.constants import OPERATION_ALLOWED_COLUMN_VALUE
from Data_Ingestion.constants import VALUE_FOR_ALLOW
import os
import asyncio
from haystack import Document, Label, Answer
from Data_Ingestion.constants import TEMPLATE_LABEL
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel
import Knowledgebase.QuestionAnswerKnowledgebase.utils as utils
from Knowledgebase.QuestionAnswerKnowledgebase.Training.Trainer import Trainer
import pandas as pd

from haystack.nodes import DensePassageRetriever
from haystack.nodes import Seq2SeqGenerator
from haystack.pipelines import GenerativeQAPipeline



class GenerativeQuestionAnswerKnowledgebase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
        self.documentStore =  utils.determineDocumentStore()

        
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
    
        self.isTraining = False
        self.trainThread : threading.Thread = None
        self.trainingCallback = None


    async def initialize(self):
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

    
        availableYears = self.dataManager.getAllAvailableYearsSorted()
        await self.writeDocToDocumentStore(availableYears, delete=True)
        self.pipeline = GenerativeQAPipeline(self.reader, self.retriever)


    def loadReader(self, loadPath, pathToSave, save=True):
        self.reader = Seq2SeqGenerator(model_name_or_path="vblagoje/bart_lfqa")
       
    def loadRetriever(self, loadPath, pathToSave, save=True):
        # self.retriever = EmbeddingRetriever(
        #     embedding_model= loadPath,
        #     document_store=self.documentStore
        # )
        # if save:
        #     self.retriever.save(pathToSave)
        self.retriever = DensePassageRetriever(
        document_store=self.documentStore,
        query_embedding_model="vblagoje/dpr-question_encoder-single-lfqa-wiki",
        passage_embedding_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki",
    )
        



    async def writeDocToDocumentStore(self, years: List[Tuple[str, str]], delete=False):
        if (delete== True):
            self.documentStore.delete_documents()
        availableYears = self.dataManager.getAllAvailableYearsSorted()
        yearAgnosticData = self.dataManager.findAllYearAngosticDataName()

        await utils.writeDocToDocumentStore(availableYears, yearAgnosticData,self.dataManager, self.documentStore, lambda x: x)
        self.documentStore.update_embeddings(self.retriever)


    def getAvailableOptions(self, intent, entities, startYear, endYear):
        raise NotImplementedError()

   
    async def searchForAnswer(self, question, intent, entitiesExtracted, startYear, endYear) -> Tuple[List[ChatbotAnswer], bool]:
    
        result = self.pipeline.run(query = question, params= {
           "Retriever": {"top_k": 3},
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

        print(result)
        answers : List[Answer] = result["answers"]
       
        print("THE RESULT")
        for answer in answers:
            print(answer.answer)
          
        chatbotAnswers : List[ChatbotAnswer]= []
       
        for answer in answers:
            # print(answer)
            # print(answer.score)
            # if answer.score < self.scoreThreshold:
            #     print("SKIP")
            #     continue
            
            chatbotAnswer = self.constructAnswer(answer, result)
            print("APPENDING")
            chatbotAnswers.append(chatbotAnswer)

        if len(chatbotAnswers) == 0:
            chatbotAnswers = self.getBackupAnswer(answers, result)

        return (chatbotAnswers, True)
    
    def constructAnswer(self, answer : Answer, result):
        # document : Document= utils.findDocumentWithId(answer.document_ids[0], result["documents"])
        # metadata=dict()
        # metadata["context"] =answer.context
        # metadata["offsets_in_document"] = answer.offsets_in_context
        # metadata["document_ids"]= answer.document_ids
        # metadata["actual answer"] = answer.answer
        # metadata["document_content"] = document.content
        # metadata["document_question"] = document.meta["query"]
        # print("DOC META")
        # print(document.meta)
        chatbotAnswer = ChatbotAnswer(answer = answer.answer, source=self.source)
        return chatbotAnswer
        # chatbotAnswers.append(chatbotAnswer)
    

    def getBackupAnswer(self, answers : List[Answer], result):
        backupAnswers = []
        for answer in answers:
            chatbotAnswer = self.constructAnswer(answer, result)
            backupAnswers.append(chatbotAnswer)
        return backupAnswers
    
    

    def train(self, trainingLabels : List[MultiFeedbackLabel], callback):
        # if self.isTraining and not self.trainThread == None:
        #     if self.trainThread.is_alive():
        #         print("TRAINING THREAD IS ALIVE")
        #         return False        

        # # try:
        #     # self.trainer.trainDataForEmbeddingRetriever(trainingLabels, self.retriever, saveDirectory=self.fullRetrieverPath,documentStore= self.documentStore, source=self.source, useQuestion=True )
        #     # self.trainer.trainDataForModelWithSQUAD(trainingLabels=trainingLabels, model=self.reader, saveDirectory= self.fullReaderPath, source=self.source)
        # trainingThread = TrainingThread("trainingThread"+str(random.random()), "traingThread", trainingLabels, self.trainer,self)
        # trainingThread.start()
        # self.trainThread = trainingThread
        # self.trainingCallback = callback
        # print("TRAINING STARTED")
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
        await utils.writeDocToDocumentStoreWithDataName([dataDict], self.dataManager, self.documentStore, lambda x: x )
        self.documentStore.update_embeddings(self.retriever)

    def dataDeleted(self, dataName):
        print("DELETE DOCUMENT")
        self.documentStore.delete_documents(filters={"dataName": dataName})
        print("________")
        print(self.documentStore.get_all_documents(filters={"dataName":dataName}))
        # self.documentStore.update_embeddings(self.retriever)





class TrainingThread (threading.Thread):
   def __init__(self, threadID, name, trainingLabels : List[MultiFeedbackLabel],trainer : Trainer, knowledgebase):
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
