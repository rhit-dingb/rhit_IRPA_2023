from typing import List
from haystack import Document
from decouple import config
from haystack.document_stores import InMemoryDocumentStore, ElasticsearchDocumentStore

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
    