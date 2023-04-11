from typing import Dict, List, Tuple
from Knowledgebase.Knowledgebase import KnowledgeBase
# from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore, ElasticsearchDocumentStore
from haystack.pipelines import  FAQPipeline, DocumentSearchPipeline


from haystack.nodes import  EmbeddingRetriever

from haystack.nodes import FARMReader
from haystack import Document, Label, Answer
from DataManager.DataManager import DataManager
from Data_Ingestion.constants import OPERATION_ALLOWED_COLUMN_VALUE
from Data_Ingestion.constants import VALUE_FOR_ALLOW
import os
import asyncio
import pandas as pd

from Data_Ingestion.constants import TEMPLATE_LABEL
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel
import Knowledgebase.QuestionAnswerKnowledgebase.utils as utils
from Knowledgebase.QuestionAnswerKnowledgebase.Training.Trainer import Trainer
from decouple import config

class  FAQKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
        self.documentStore = utils.determineDocumentStore()
        self.reader = None
        self.pipeline = None
        self.retriever = None
        # self.dataFetcher = DataFetcher()
        self.trainedModelPath = "TrainedModels\FAQModel"
        self.source = "FAQKnowledgebase"
        dirname = os.path.dirname(__file__)
        self.fullModelPath = os.path.join(dirname, self.trainedModelPath)   
        self.trainer = Trainer()


    def loadStartingModel(self, pathToSave):
        print("LOAD START MODEL")
        self.retriever = EmbeddingRetriever(
            document_store=self.documentStore,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            use_gpu=True,
        )

        # self.retriever.save(pathToSave)
        print("AFter SAVE")
        print(self.retriever)


    async def initialize(self):
        if not os.path.exists(self.fullModelPath):
            os.makedirs(self.fullModelPath)

        
        dir = os.listdir(self.fullModelPath)
        if len(dir) == 0:
            self.retriever = EmbeddingRetriever(
                document_store=self.documentStore,
                embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
                use_gpu=True,
            )    
            self.retriever.save(self.fullModelPath)

            #self.loadStartingModel(fullPath)
        else:
            print("LOAD ALREADY SAVED MODEL")
            self.retriever = EmbeddingRetriever(
            document_store=self.documentStore,
            embedding_model=self.fullModelPath,
            use_gpu=True,
            )
            
            print(self.retriever.model_format)
            print(self.retriever)

        availableYears = self.dataManager.getAllAvailableYearsSorted()
        await self.writeDocToDocumentStore(availableYears)
        self.pipeline = FAQPipeline(retriever=self.retriever)
      


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
                            if (OPERATION_ALLOWED_COLUMN_VALUE in newDoc.meta) and newDoc.meta[OPERATION_ALLOWED_COLUMN_VALUE] == VALUE_FOR_ALLOW:
                                continue

                            if TEMPLATE_LABEL in document.meta:
                                continue
                            
                            documents.append(newDoc)
                       

                        df= self.convertToDf(documents)
                        
                        docs_to_index = df.to_dict(orient="records")
                        self.documentStore.write_documents(docs_to_index)
        print("ALL DOCS")
        print(self.documentStore.get_all_documents())
        self.documentStore.update_embeddings(self.retriever)
      

    def convertToDf(self,documents : List[Document]):

        data = [[doc.meta["query"], doc.content] for doc in documents]
        df = pd.DataFrame(data= data, columns=["question", "answer"])
        df.fillna(value="", inplace=True)
        
        df["question"] = df["question"].apply(lambda x: x.strip())
        questions = list(df["question"].values)
        df["embedding"] = self.retriever.embed_queries(queries=questions).tolist()
        df = df.rename(columns={"question": "content"})
        if(len(documents)>0):
        # add rest of metadata
            for key in documents[0].meta:
                df[key] = [documents[0].meta[key]] * len(documents)
        
        #Add id
        ids = [document.id for document in documents]
        df["id"] = ids
            
        return df
    
            

    def loadStartingModel(self, pathToSave):
        pass

    def getAvailableOptions(self, intent, entities, startYear, endYear):
        raise NotImplementedError()

   
    async def searchForAnswer(self, question, intent, entitiesExtracted,startYear, endYear):
         # create qa pipeline
        print("SEARCH FOR ANSWER")
        result = self.pipeline.run(query = question, params= {
          
            "Retriever": {"top_k": 5}, 
            
            "filters": {
                "startYear": str(startYear),
                "endYear": str(endYear)
            }
        }
        
        )   
        answers : List[Answer] = result["answers"]
        print("THE RESULT")
        print(result)
        chatbotAnswers : List[ChatbotAnswer]= []
        for answer in answers:
            document : Document= utils.findDocumentWithId(answer.document_ids[0], result["documents"])
            
            metadata=dict()
            metadata["context"] =answer.context
            metadata["offsets_in_context"] = answer.offsets_in_context
            metadata["document_ids"]= answer.document_ids
            metadata["document_content"] = document.content
            #answerStrings.append(answer.answer)
            chatbotAnswer = ChatbotAnswer(answer = answer.answer, source=self.source, metadata=metadata)
            chatbotAnswers.append(chatbotAnswer)

        return chatbotAnswers
    
    
        
    def aggregateDiscreteRange(self, entities, dataModel, isSumming):
        raise NotImplementedError()


    def calculatePercentages(self, searchResults, entitiesForEachResult, dataModel):
        raise NotImplementedError()


    async def train(self, trainingLabels : List[MultiFeedbackLabel]):
        self.trainer.trainDataForEmbeddingRetriever(trainingLabels, retriever = self.retriever, saveDirectory= self.fullModelPath, documentStore = self.documentStore, source=self.source)
        availableYears = self.dataManager.getAllAvailableYearsSorted()       

        # reload model.
        self.retriever = EmbeddingRetriever(
            document_store=self.documentStore,
            embedding_model=self.fullModelPath,
            use_gpu=True,
        )
        # await self.writeDocToDocumentStore(availableYears)
        
        self.documentStore.update_embeddings(self.retriever)
    
    def dataUploaded(self):
        pass

    def dataDeleted(self):
        pass  



