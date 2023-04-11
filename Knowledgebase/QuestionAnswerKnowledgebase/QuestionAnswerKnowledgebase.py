from typing import Dict, List, Tuple
from Knowledgebase.Knowledgebase import KnowledgeBase
from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline,  FAQPipeline, DocumentSearchPipeline
from haystack.nodes import FARMReader
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

class QuestionAnswerKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
        self.documentStore =  utils.determineDocumentStore()
        self.trainedModelPath = "TrainedModels\QAModel"
        self.startingModel = "deepset/roberta-base-squad2"
        self.retriever = EmbeddingRetriever(
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            document_store=self.documentStore
        )
        self.yearToDocumentStore = dict()
        self.source = "QuestionAnswerKnowledgebase"
        dirname = os.path.dirname(__file__)
        self.fullModelPath = os.path.join(dirname, self.trainedModelPath)   
        self.reader = None
        self.pipeline = None


    async def initialize(self):
        if not os.path.exists(self.fullModelPath):
            os.makedirs(self.fullModelPath)

        # dirname = os.path.dirname(__file__)
        # fullPath = os.path.join(dirname, self.trainedModelPath)   
        dir = os.listdir(self.fullModelPath)
        if len(dir) == 0:
            self.loadStartingModel(self.fullModelPath)
        else:
            self.reader = FARMReader(model_name_or_path=self.fullModelPath, use_gpu=True, context_window_size=1000)

        availableYears = self.dataManager.getAllAvailableYearsSorted()
        await self.writeDocToDocumentStore(availableYears)
        self.pipeline = ExtractiveQAPipeline(self.reader, self.retriever)


    async def writeDocToDocumentStore(self, years: List[Tuple[str, str]]):
        self.documentStore.delete_documents()
        for startYear, endYear in years:
           availableDataName = self.dataManager.getAvailableDataForSpecificYearRange(startYear, endYear)
           for dataName in availableDataName:
               sections = self.dataManager.getSections(dataName)
               for section in sections:
                    subsectionToDocument : Dict[str, Document] = await self.dataManager.getDataByStartEndYearAndIntent(section, startYear, endYear, Exception()) 
                    
                    for key in subsectionToDocument:
                        documents = []
                        documentList = subsectionToDocument[key]
                        for document in documentList:
                          
                            metaData = document.meta.copy()
                            metaData["startYear"] = str(startYear)
                            metaData['endYear'] = str(endYear)
                            newDoc =  Document(id_hash_keys=["content", "meta"], content = document.content,meta=metaData )
                            #print(document.meta)
                            if (OPERATION_ALLOWED_COLUMN_VALUE in document.meta) and document.meta[OPERATION_ALLOWED_COLUMN_VALUE] == VALUE_FOR_ALLOW:
                                print("DISALLOWING", key )
                                continue

                            if TEMPLATE_LABEL in document.meta:
                                continue
                        
                            documents.append(newDoc)

                        print("ADDED", len(documents), "FOR", key)
                        self.documentStore.write_documents(documents)
        self.documentStore.update_embeddings(self.retriever)



    def loadStartingModel(self, pathToSave):
        self.reader = FARMReader(model_name_or_path=self.startingModel, use_gpu=True, context_window_size=1000)
        self.reader.save(pathToSave)
        self.reader = FARMReader(model_name_or_path=self.trainedModelPath, use_gpu=True, context_window_size=1000)
        print("LOADED READER", self.reader)


    def getAvailableOptions(self, intent, entities, startYear, endYear):
        raise NotImplementedError()


   
    async def searchForAnswer(self, question, intent, entitiesExtracted,startYear, endYear):
        
        result = self.pipeline.run(query = question, params= {
            "Retriever": {"top_k": 10}, 
            "Reader": {"top_k": 5},
            "filters": {
            "startYear": startYear,
            "endYear": endYear
             }
        })

        answers : List[Answer] = result["answers"]
        chatbotAnswers : List[ChatbotAnswer]= []
       
        for answer in answers:
            document : Document= utils.findDocumentWithId(answer.document_ids[0], result["documents"])
            metadata=dict()
            metadata["context"] =answer.context
            metadata["offsets_in_document"] = answer.offsets_in_context
            metadata["document_ids"]= answer.document_ids
            metadata["actual answer"] = answer.answer
            metadata["document_content"] = document.content
            chatbotAnswer = ChatbotAnswer(answer = answer.context, source=self.source, metadata= metadata)
            chatbotAnswers.append(chatbotAnswer)

        return chatbotAnswers
    
    # def provideFeedback(self):
    #     self.documentStore.write_labels

 
    def aggregateDiscreteRange(self, entities, dataModel, isSumming):
        raise NotImplementedError()


    def calculatePercentages(self, searchResults, entitiesForEachResult, dataModel,):
        raise NotImplementedError()


    def train(self, trainingLabels : List[MultiFeedbackLabel]):
        pass
    
    def dataUploaded(self):
        pass

    def dataDeleted(self):
        pass  



