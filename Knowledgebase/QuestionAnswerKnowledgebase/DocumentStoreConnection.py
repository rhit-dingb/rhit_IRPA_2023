
from decouple import config
import requests
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


class DocumentStoreConnection():
    def __init__(self):
        pass


    def determineDocumentStore(self):
        """
        Determine which document store to use based on the environment 
        """
        try:
            environment = config('ENVIRONMENT')

            if environment == "development":
                return InMemoryDocumentStore()
            elif environment == "production":
                elasticSearch = ElasticsearchDocumentStore()
                self.setElasticSearchDiskLimit()
                return elasticSearch
        except Exception: 
            print("NO ENV FILE, Using InMemoryDocumentStore")
            return InMemoryDocumentStore()



    def setElasticSearchDiskLimit(self):
      
        # Cluster settings request to set disk watermarks
        cluster_settings_url = "http://localhost:9200/_cluster/settings"
        cluster_settings_payload = {
            "persistent": {
                "cluster.routing.allocation.disk.watermark.low": "90%",
                "cluster.routing.allocation.disk.watermark.high": "95%",
                "cluster.routing.allocation.disk.watermark.flood_stage": "99%"
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.put(cluster_settings_url, headers=headers, json=cluster_settings_payload)
        print(response.json())

        # Index settings request to remove read-only flag
        index_settings_url = "http://localhost:9200/*/_settings?expand_wildcards=all"
        index_settings_payload = {"index.blocks.read_only_allow_delete": None}
        response = requests.put(index_settings_url, headers=headers, json=index_settings_payload)
        print(response.json())

   

    async def writeDocToDocumentStore(self, years: List[Tuple[str, str]], yearAgnosticDataNames : List[str], dataManager : DataManager, documentStore : BaseDocumentStore, process_doc_func):
        """
        Given a list of available years that data is available and a list of year agnostic data names, write all the data for all the available year and the
        year agnostic data to the document store. 

        :param years: A list of tuple, each tuple has two elements. The first element is the start year and the second element is the end year.

        :param dataManager: instance of DataManager's concrete class to fetch documents(qa pair) from the data source.
        
        :param documentStore: DocumentStore to write the documents to.

        :param process_doc_func: A function used to process the document and make any changes to it before writing to the document store
        """

        # print("WRITE TO DOCUMENT STORE")
        # print(years)
        dataNamesDicts = []
        for startYear, endYear in years:
            availableDataName = dataManager.getAvailableDataForSpecificYearRange(startYear, endYear)
            for dataName in availableDataName:
                dataNamesDicts.append({"dataName": dataName, "startYear": startYear, "endYear": endYear})

        for dataName in yearAgnosticDataNames:
            dataNamesDicts.append({"dataName":dataName})

        await self.writeDocToDocumentStoreWithDataName(dataNamesDicts, dataManager, documentStore, process_doc_func)
        

    async def writeDocToDocumentStoreWithDataName(self, dataNameDicts : List[Dict[str,str]], dataManager : DataManager, documentStore : BaseDocumentStore, process_doc_func):
        """
        Given a list of dataName data dicitonaries, data manager, and document store, and a function to process each document, this functin will 
        write all the data for each given data name to the document store and appending necessary metadata for each document as well.

        :param dataNameDicts: A list of dictionary object containing necessary neccesary info about each data. For example:
        {
            "dataName":"CDS_2020_2021",
            "startYear": 2020,
            "endYear": 2021
        }

        or for year agnostic data:

        {
            "dataName":"CDS_2020_2021",
        }


        :param dataManager: DataManager class instance to interface with the backend data source
        :param documentStore: The document store to store the documents into.
        :param process_doc_func: A function used to process the document and make any changes to it before writing to the document store
        """
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
                # try:
                subsectionToDocument : Dict[str, List[Document]] = await dataManager.getDataBySection(section,Exception(), startYear, endYear) 
                # print("SUBSECTION TO DOCUMENT")
                # print(subsectionToDocument)
                # except Exception:
                #     continue

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
                    # print("WRITING", dataName, "Subsection", key )
                    documentStore.write_documents(processed_docs)
    
