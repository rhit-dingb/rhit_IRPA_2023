from typing import List
from haystack import Label
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel
from haystack.nodes import  EmbeddingRetriever


class Trainer:
    def __init__(self):
        pass

    def trainEmbeddingRetriever(label : List[Label]):
        pass


class TrainingDataCreator:
    def __init__(self):
        pass

    def createTrainingDataForEmbeddingRetriever(self, trainingLabels : List[MultiFeedbackLabel]):
        pass
