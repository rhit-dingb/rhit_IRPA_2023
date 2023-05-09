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

"""
Contain util functions for QuestionAnswerKnowledgebase
"""


def findDocumentWithId(id: str, documents : List[Document]) -> Document:
        for doc in documents:
            if doc.id == id:
                return doc
            
        return None

