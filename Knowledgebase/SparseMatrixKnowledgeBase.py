from logging import raiseExceptions
from re import I
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
        
    """
    This function will search in the sparse matrices retrieved by the given intent and calculate the total sum 
    based on the shouldAddRowStrategy.
    intent: intent of the user message
    entitiesExtracted: list entities extracted by user input, each individual element is an object with the entity label, value and other information
    shouldAddRowStrategy: for each row, this function will determine if we should add the value of this row to the total sum.
    Return: answer calculated and returned as string.
    """
    def searchForAnswer(self, intent, entitiesExtracted, shouldAddRowStrategy):
        count=0
        col_index=0

        #this list contains the value of the entities extracted.
        entities = []
        for entityObj in entitiesExtracted:
            entities.append(entityObj["value"])

        sparseMatrices = self.data[intent]
        sparseMatrixToSearch = self.determineMatrixToSearch(sparseMatrices, entities)
        if sparseMatrixToSearch is None:
            raise Exception("No valid sparse matrix found for given intent and entities", intent, entities)
        
        for i in range(sparseMatrixToSearch.shape[0]):
            if sparseMatrixToSearch.loc[i,"total"] == 1:
                continue

            row = sparseMatrixToSearch.loc[i]
            shouldAdd = shouldAddRowStrategy.determineShouldAddRow(row, entities)
            if shouldAdd:
                #print("Im ADDING " + str(self.m_df.loc[i,'Value']))
                count += sparseMatrixToSearch.loc[i,'Value']
                
        return str(count)    




    def searchForAnswerBasic(self, intent, entities):
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

    """
    This function will determine which sparse matrix under an intent should we search based on the given entities.
    For each sparse matrix, it will calculate the number of entities that the sparse matrix has corresponding columns for.
    Then this function will find and return sparse matrix with the highest match number.
    We do this because for example, for enrollment, there are two matrix, one for general enrollment info and one for enrollment by race
    and if the user asks something like "how many hispanics male student are enrolled?" Should we use the general matrix that has gender
    or should we use the enrollment by race that has information on hispanic student enrollment?  
    If enrollment by race matrix has information about hispanic male enrollment, this algorithm would choose that. But in this cause,
    there is no such information and it is out of scope, so we can use any matrix, it will return 0 anywas.

    For now, we will always use the last matrix if there is a tie.
    """
    def determineMatrixToSearch(self, sparseMatrices, entities,):
        maxMatch = []
        currMax = 0
        for sparseMatrix in sparseMatrices:
            entitiesMatchCount = 0
            for entity in entities:
                if entity in sparseMatrix.columns:
                    entitiesMatchCount = entitiesMatchCount+1
                    
            if entitiesMatchCount>currMax:
                maxMatch = []
                maxMatch.append(sparseMatrix)
                currMax = entitiesMatchCount
            elif entitiesMatchCount == currMax:
                maxMatch.append(sparseMatrix)


        return maxMatch[len(maxMatch)-1]

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


  
