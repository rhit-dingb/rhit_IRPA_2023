
from html import entities
from tracemalloc import start
from DataManager.DataManager import DataManager
from Data_Ingestion.SparseMatrix import SparseMatrix
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.Knowledgebase import KnowledgeBase
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import pandas as pd
import numpy as np

from Knowledgebase.Knowledgebase import KnowledgeBase

from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController.output import  identityFunc, outputFuncForPercentage

from actions.entititesHelper import copyEntities


class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager = dataManager

    """
    This function will search in the sparse matrices retrieved by the given intent and calculate the total sum 
    based on the shouldAddRowStrategy.
    intent: intent of the user message

    entitiesExtracted: list of entities extracted by user input, each individual element is an object with the entity label, value and other information
    or this could be a list of entities used to gather information for an aggregation method, in this case, the entities could be fake or real entities from user input.

    shouldAddRowStrategy: for each row, this function will determine if we should add the value of this row to the total sum.

    Return: answer calculated and returned as string.

    Throws: exception when given year or intent for the data is not found or when exception encountered when parsing year entity values

    """
    def searchForAnswer(self, intent, entitiesExtracted, shouldAddRowStrategy, outputFunc = identityFunc, initialValue = 0):
        count = initialValue
        col_index=0

        #this list contains the value of the entities extracted.
        entities = []
        usedEntities = []
        printEntities = []
        
        for entityObj in entitiesExtracted:
            entities.append(entityObj["value"])

        
        sparseMatrixToSearch : SparseMatrix; startYear : str; endYear : str 
        sparseMatrixToSearch, startYear, endYear = self.determineMatrixToSearch(intent, entitiesExtracted)
        
        if sparseMatrixToSearch is None:
            raise Exception("No valid sparse matrix found for given intent and entities", intent, entities)

        # get the underlying pandas dataframe from the internal data model
        sparseMatrixToSearch = sparseMatrixToSearch.getSparseMatrixDf()
        print("SPARSEMATRIX")
        print(sparseMatrixToSearch)
        for i in range(sparseMatrixToSearch.shape[0]):
            row = sparseMatrixToSearch.loc[i]
            
            if "total" in row.index and sparseMatrixToSearch.loc[i,"total"] == 1:
                continue
           
            usedEntities = shouldAddRowStrategy.determineShouldAddRow(row, entities)
            # print(usedEntities)
            if len(usedEntities) > 0:
               
                count += sparseMatrixToSearch.loc[i,'Value']
                if len(printEntities) <= 0:
                    printEntities = usedEntities
                    
        printEntities = list(printEntities)
        printEntities.append(startYear) 
        return outputFunc(count, intent, printEntities)



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
                print("Im ADDING " + str(self.m_df.loc[i,'Value']))
                count += sparseMatrixToSearch.loc[i,'Value']
                
        return str(count)


    def aggregateDiscreteRange(self, intent, filteredEntities, start, end, generator, shouldAddRow, outputFunc):
        shouldAddRowStrategy = shouldAddRow
        total = 0
        # print(start,end)
        entitiesUsed = []
        
        for i in range(start, end+1):
            filteredEntitiesCopy = copyEntities(filteredEntities)
            entityValue = generator(i, start, end)
            # we can make the entity key more descriptive later 
            fakeEntity = {
                "entity": "graduation_years",
                "value": entityValue,
                "aggregation": True
            }
        
            filteredEntitiesCopy.append(fakeEntity)
           
            answer, intent, entitiesUsedBySearch = self.searchForAnswer(intent, filteredEntitiesCopy, shouldAddRowStrategy, identityFunc)
            entitiesUsed = entitiesUsed + list(entitiesUsedBySearch)
            
            total = total + int(answer)
         
 
        return outputFunc(total, intent, set(entitiesUsed))

    def aggregatePercentage(self, intent, numerator, entitiesForNumerator, entitiesToCalculateDenominator, shouldAddRowStrategy):
        entitiesUsed = None
        
        denominator,intent, entitiesUsed = self.searchForAnswer(intent, entitiesToCalculateDenominator, shouldAddRowStrategy, identityFunc)
        percentageCalc = numerator/float(denominator)*100
        percentage = round(percentageCalc, 1)
        
        return outputFuncForPercentage(percentage, intent, set(list(entitiesUsed)+ list(entitiesForNumerator)) )


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


  
