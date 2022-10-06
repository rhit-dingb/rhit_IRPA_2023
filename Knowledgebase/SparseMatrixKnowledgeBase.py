from logging import raiseExceptions
from Knowledgebase.Knowledgebase import KnowledgeBase
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import pandas as pd
import copy
import numpy as np

from Knowledgebase.Knowledgebase import KnowledgeBase
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import copy
class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, filePath):
        self.excelProcessor = ExcelProcessor()
        self.topicToParse = ["enrollment"]
        self.data = self.excelProcessor.processExcelSparse(filePath, self.topicToParse)

        #self.m_df = self.data["General_Enrollment"] # this is HARD CODED NOW

    def shouldRowBeAdded(row, entities):
        if row has all column marked as 1 corresponding to given entities and row has no extra column marked as 1:
            return true

        else:
            return false


    def searchForAnswer(self, intent, entities, lambda):
        count=0
        col_index=0
        #TODO filter out entities that are not under this intent
        sparseMatrices = self.data[intent]
        sparseMatrixToSearch = self.determineMatrixToSearch(sparseMatrices, entities)
        if sparseMatrixToSearch is None:
            raise Exception("No valid sparse matrix found for given intent and entities", intent, entities)
        
        for i in range(sparseMatrixToSearch.shape[0]):
            temp_count = 0
            if sparseMatrixToSearch.loc[i,"total"] == 1:
                continue

            for entity in sparseMatrixToSearch.columns:
                if entity in entities: 
                    if sparseMatrixToSearch.loc[i,entity] == 1:
                        temp_count += 1
            if temp_count == len(entities):
                #print("Im ADDING " + str(self.m_df.loc[i,'Value']))
                count += sparseMatrixToSearch.loc[i,'Value']
                
        return str(count)

    def determineMatrixToSearch(self, sparseMatrices, entities):
        entitiesMatchCountForEachMatrix = []
        for sparseMatrix in sparseMatrices:
            entitiesMatchCount = 0
            for entity in entities:
                if entity in sparseMatrix.columns:
                    entitiesMatchCount = entitiesMatchCount+1
            entitiesMatchCountForEachMatrix.append(entitiesMatchCount)

        index = entitiesMatchCountForEachMatrix.index(max(entitiesMatchCountForEachMatrix))
        return sparseMatrices[index]

    def dummyRandomGeneratedDF(self):
        self.m_df = pd.DataFrame()
        self.m_df['Value'] = np.floor(np.random.uniform(low= 20, high=2000, size=(20,)))
        self.m_df['undergraduate'] = np.random.choice([0, 1], size=20, p=[.5, .5])
        self.m_df['grad'] = np.random.choice([0, 1], size=20, p=[.5, .5])
        self.m_df['male'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['female'] = np.random.choice([0, 1], size=20, p=[.6, .4])
        self.m_df['degree-seeking'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['non-degree-seeking'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['full-time'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['part-time'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['freshman'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['non-freshman'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['first-year'] = np.random.choice([0, 1], size=20, p=[.7, .3])
        self.m_df['white'] = np.random.choice([0, 1], size=20, p=[.9, .1])
        self.m_df['african American'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['asian'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['hispanic'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['pacific islander'] = np.random.choice([0, 1], size=20, p=[.8, .2])
        self.m_df['two or more races'] = np.random.choice([0, 1], size=20, p=[.9, .1])
        self.m_df['ethinicity unknown'] = np.random.choice([0, 1], size=20, p=[.6, .4])
        self.m_df['Total?'] = np.random.choice([0, 1], size=20, p=[.9, .1])


  
