from logging import raiseExceptions
from re import I
from DataManager.DataManager import DataManager
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.Knowledgebase import KnowledgeBase
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import pandas as pd
import copy
import numpy as np

from Knowledgebase.Knowledgebase import KnowledgeBase

import copy

from actions.entititesHelper import copyEntities


class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager = dataManager

    """
    This function will search in the sparse matrices retrieved by the given intent and calculate the total sum 
    based on the shouldAddRowStrategy.
    intent: intent of the user message
    entitiesExtracted: list entities extracted by user input, each individual element is an object with the entity label, value and other information
    shouldAddRowStrategy: for each row, this function will determine if we should add the value of this row to the total sum.
    Return: answer calculated and returned as string.

    Throws: exception when given year or intent for the data is not found or when exception encountered when parsing year entity values

    """
    def searchForAnswer(self, intent, entitiesExtracted, shouldAddRowStrategy):
        count=0
        col_index=0

        #this list contains the value of the entities extracted.
        entities = []
        for entityObj in entitiesExtracted:
            entities.append(entityObj["value"])

        
        sparseMatrixToSearch, startYear, endYear = self.determineMatrixToSearch(intent, entitiesExtracted)
      
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
                
        return str(int(count))    




    def searchForAnswerBasic(self, intent, entities):
        count=0
        col_index=0
        #TODO filter out entities that are not under this intent
        
        sparseMatrixToSearch = self.determineMatrixToSearch(intent, entities)
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

    def aggregateDiscreteRange(self, intent, filteredEntities, start, end, generator, shouldAddRow):
        shouldAddRowStrategy = shouldAddRow
        total = 0
       
        for i in range(start, end+1):
            filteredEntitiesCopy = copyEntities(filteredEntities)
            entityValue = generator(i, start, end)
            # we can make the entity key more descriptive later 
            fakeEntity = {
                "entity": i,
                "value": entityValue,
                "isFake": True
            }
            
            filteredEntitiesCopy.append(fakeEntity)
             
            answer = self.searchForAnswer(intent, filteredEntitiesCopy, shouldAddRowStrategy )
            total = total + int(answer)

        return str(total)


    def determineMatrixToSearch(self, intent, entities):
        return self.dataManager.determineMatrixToSearch(intent, entities)


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


  
