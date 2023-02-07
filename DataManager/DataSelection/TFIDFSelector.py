

from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from actions.entititesHelper import getEntityValueHelper

class TFIDFSelector():
    def __init__(self):
        pass

    
    def selectBest(self, questionEntities, entityForData : List[List[str]]):
        vectorizer = TfidfVectorizer()
        entityStrings = []
        for entityList in entityForData:
            entityStr = " ".join(entityList)
            entityStrings.append(entityStr)
        
        questionEntitiesValue = getEntityValueHelper(questionEntities)
        tfidf_matrix = vectorizer.fit_transform(entityStrings)
        question_vector = vectorizer.transform([" ".join(questionEntitiesValue)])
        # print("______________________")
        # print(question_vector.shape)
        # print(tfidf_matrix.shape)
        similarities = cosine_similarity(question_vector, tfidf_matrix)
        best_index = similarities.argmax()
        return best_index
        
        