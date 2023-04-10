
from typing import Dict, List
from Data_Ingestion.MongoProcessor import MongoProcessor
from haystack import Document, Label
from Data_Ingestion.SubsectionQnA import SubsectionQnA
import uuid

class ConvertToDocumentDecorator():
    def __init__(self, decorated):
        self.decorated : MongoProcessor = decorated 


    async def getDataByDbNameAndIntent(self, client, intent, dbName) -> Dict[str, Document]:
        subsectionQnAList : List[SubsectionQnA] = await self.decorated.getDataByDbNameAndIntent(client, intent, dbName)
        subsectionToDocument : Dict[str, Document] = {subsectionQnA.subSectionName: [] for subsectionQnA in subsectionQnAList }
        for subsectionQnA in subsectionQnAList :
               
                for questionAnswer in subsectionQnA.questionAnswers:
                   # print("CONTENT", subsectionQnA.questionAnswers[questionAnswer] )
                    subsectionQnA.metadata["query"] = questionAnswer
                    subsectionQnA.metadata["subsection"] = subsectionQnA.subSectionName
                    document = Document( id_hash_keys=["content", "meta"], content= subsectionQnA.questionAnswers[questionAnswer],
                        meta=subsectionQnA.metadata.copy())
                   
                    subsectionToDocument[subsectionQnA.subSectionName].append(document)
        
        return subsectionToDocument