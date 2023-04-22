import re
from typing import Dict, List, Tuple
from haystack import Document
from decouple import config
from haystack.document_stores import InMemoryDocumentStore, ElasticsearchDocumentStore, BaseDocumentStore
from DataManager.DataManager import DataManager
from Data_Ingestion.constants import OPERATION_ALLOWED_COLUMN_VALUE
from Data_Ingestion.constants import VALUE_FOR_ALLOW
from Data_Ingestion.constants import TEMPLATE_LABEL
from DataManager.constants import ANNUAL_DATA_REGEX_PATTERN, DEFINITION_DATA_REGEX_PATTERN

def findDocumentWithId(id: str, documents : List[Document]) -> Document:
        for doc in documents:
            if doc.id == id:
                return doc
            
        return None


def determineDocumentStore():
    environment = config('ENVIRONMENT')
    if environment == "development":
         return InMemoryDocumentStore()
    elif environment == "production":
         return ElasticsearchDocumentStore()
    


async def writeDocToDocumentStore(years: List[Tuple[str, str]], yearAgnosticDataName : List[str], dataManager : DataManager, documentStore : BaseDocumentStore, process_doc_func):
    
    dataNamesDicts = []
    for startYear, endYear in years:
        availableDataName = dataManager.getAvailableDataForSpecificYearRange(startYear, endYear)
        for dataName in availableDataName:
            dataNamesDicts.append({"dataName": dataName, "startYear": startYear, "endYear": endYear})

    for dataName in yearAgnosticDataName:
        dataNamesDicts.append({"dataName":dataName})

    await writeDocToDocumentStoreWithDataName(dataNamesDicts, dataManager, documentStore, process_doc_func)
    

async def writeDocToDocumentStoreWithDataName(dataNameDicts : List[Dict[str,str]], dataManager : DataManager, documentStore : BaseDocumentStore, process_doc_func):
    
    for dataNameDict in dataNameDicts:
        dataName = dataNameDict["dataName"]
        startYear = None
        endYear = None
        if "startYear" in dataNameDict:
            startYear = dataNameDict["startYear"]
        
        if "endYear" in dataNameDict:
            endYear = dataNameDict["endYear"]

        sections = dataManager.getSections(dataName)
       
        for section in sections:
          
            subsectionToDocument = dict()
            try:
                subsectionToDocument : Dict[str, List[Document]] = await dataManager.getDataBySection(section,Exception(), startYear, endYear) 
            except Exception:
                continue

            for key in subsectionToDocument:
                documents = []
                documentList = subsectionToDocument[key]
                for document in documentList:
                    metaData = document.meta.copy()
                    if startYear and endYear:
                        metaData["startYear"] = str(startYear)
                        metaData['endYear'] = str(endYear)
                        metaData["isYearAgnostic"] = False
                    else: 
                        metaData["isYearAgnostic"] = True

                    metaData["dataName"] = dataName
                    newDoc =  Document(id_hash_keys=["content", "meta"], content = document.content,meta=metaData )
                    if (OPERATION_ALLOWED_COLUMN_VALUE in newDoc.meta) and newDoc.meta[OPERATION_ALLOWED_COLUMN_VALUE] == VALUE_FOR_ALLOW:
                        continue

                    if TEMPLATE_LABEL in document.meta:
                        continue
                    
                    documents.append(newDoc)
                processed_docs = process_doc_func(documents)
                print("WRITING", dataName, "Subsection", key )
                documentStore.write_documents(processed_docs)
    
