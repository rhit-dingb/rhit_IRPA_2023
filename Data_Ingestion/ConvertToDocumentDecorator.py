
from typing import Dict, List
from Data_Ingestion.DataDecorator import DataDecorator
from Data_Ingestion.MongoProcessor import MongoProcessor
from haystack import Document, Label
from Data_Ingestion.SubsectionQnA import SubsectionQnA

class ConvertToDocumentDecorator(DataDecorator):
    """
    Class that wraps the MongoProcessor and takes the list of SubsectionQnA class and convert them to a list of 
    Document instance used by Haystack document store.
    """
   


    async def getDataByDbNameAndSection(self, client,section, dbName) -> Dict[str, Document]:
        subsectionQnAList : List[SubsectionQnA] = await self.decorated.getDataByDbNameAndSection(client, section, dbName)
        subsectionToDocument : Dict[str, Document] = {subsectionQnA.subSectionName: [] for subsectionQnA in subsectionQnAList }
        for subsectionQnA in subsectionQnAList :
               
                for questionAnswer in subsectionQnA.questionAnswers:
                   # print("CONTENT", subsectionQnA.questionAnswers[questionAnswer] )
                   
                    subsectionQnA.metadata["query"] = questionAnswer.lower()
                    subsectionQnA.metadata["subsection"] = subsectionQnA.subSectionName
                    document = Document( id_hash_keys=["content", "meta"], content= subsectionQnA.questionAnswers[questionAnswer],
                        meta=subsectionQnA.metadata.copy())
                   
                    subsectionToDocument[subsectionQnA.subSectionName].append(document)
        
        return subsectionToDocument