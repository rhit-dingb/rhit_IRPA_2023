from typing import List
from haystack import Document
def findDocumentWithId(id: str, documents : List[Document]) -> Document:
        for doc in documents:
            if doc.id == id:
                return doc
            
        return None