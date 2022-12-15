
from ast import List
from typing import Tuple
from DataManager.DataManager import DataManager
from DataManager.constants import NUMBER_ENTITY_LABEL, RANGE_ENTITY_LABEL
from Data_Ingestion.SparseMatrix import SparseMatrix
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.Knowledgebase import KnowledgeBase
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import pandas as pd
import numpy as np

from Knowledgebase.Knowledgebase import KnowledgeBase
from Knowledgebase.RangeExactMatchRowStrategy import  RangeExactMatchRowStrategy
from Knowledgebase.SearchResultType import SearchResultType
from Knowledgebase.TypeController import TypeController

from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController.output import  constructSentence, identityFunc, outputFuncForPercentage
from actions.constants import RANGE_MORE_THAN_VALUE, RANGE_UPPER_BOUND_VALUE

from actions.entititesHelper import copyEntities, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper


class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
        self.typeController = TypeController()
        self.year = dataManager.getMostRecentYearRange()[0]

    
    def setYear(self,year):
        self.year = year


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
    def searchForAnswer(self, intent, entitiesExtracted, shouldAddRowStrategy, outputFunc, shouldAdd = True):
        print("BEGAN SEARCHING")
        searchResults = []

        searchResult = None

        #this list contains the value of the entities extracted.
        entities = []
        usedEntities = []
        printEntities = []
        
        for entityObj in entitiesExtracted:
            entities.append(entityObj["value"])

        sparseMatrixToSearch : SparseMatrix; startYear : str; endYear : str 
        sparseMatrixToSearch, startYear, endYear = self.determineMatrixToSearch(intent, entitiesExtracted, self.year)
        
        if sparseMatrixToSearch is None:
            raise Exception("No valid sparse matrix found for given intent and entities", intent, entities)
        # get the underlying pandas dataframe from the internal data model
        sparseMatrixToSearchDf = sparseMatrixToSearch.getSparseMatrixDf()
        for i in range(sparseMatrixToSearchDf.shape[0]):
            row = sparseMatrixToSearchDf.loc[i]
            
            if "total" in row.index and sparseMatrixToSearchDf.loc[i,"total"] == 1:
                continue
           
            shouldUseRow, usedEntities = shouldAddRowStrategy.determineShouldAddRow(row, entities, sparseMatrixToSearch)
            # print(usedEntities)
           
            if shouldUseRow:
                newSearchResult = sparseMatrixToSearchDf.loc[i,'Value']
                if searchResult == None: 
                    searchResult, type = self.determineResultType(newSearchResult)
                    searchResult = str(searchResult)
                    searchResults.append(searchResult)
                else:
                    searchResult = self.addSearchResult(searchResult, newSearchResult, searchResults)

                if len(printEntities) <= 0:
                    printEntities = usedEntities
                
        printEntities = list(printEntities)
        printEntities.append(startYear) 
        print(intent)
        # print(self.determineResultType(searchResult))
        print("SEARCH RESULT")
        print(searchResults)
        return outputFunc(searchResults, intent, printEntities)


    def constructOutput(self, searchResult, intent, entitiesUsed):
       #return searchResult
       return constructSentence(searchResult, intent, entitiesUsed)

    #This function will try to add up the search results, if the current search result and the new search result's type does not make sense
    # to be added together, it will add it into the list of answers instead of adding up the value.

    def addSearchResult(self, currentSearchResult, newSearchResult, searchResults) -> str:
        castedCurrValue, currentSearchResultType = self.determineResultType(currentSearchResult)
        castedNewValue, newSearchResultType = self.determineResultType(newSearchResult)
        if (currentSearchResultType == SearchResultType.FLOAT or currentSearchResultType == SearchResultType.NUMBER):
            if newSearchResultType == SearchResultType.FLOAT or newSearchResultType == SearchResultType.NUMBER:
            
                newCalculatedValue = str(castedCurrValue + castedNewValue)
                searchResults[len(searchResults)-1] = newCalculatedValue
                return newCalculatedValue
            else:
                searchResults.append(newSearchResult)
                return newSearchResult

        else:
            searchResults.append(newSearchResult)

        return newSearchResult
    
    #This function will determine the type of value the search result is: integer, float, string, percentage(string with % sign) 
    # and return the casted value along with enum value associated with that 
    def determineResultType(self,searchResult) -> Tuple[any, SearchResultType]:
        return self.typeController.determineResultType(searchResult)

    def findRange(self, entitiesFound, maxBound, minBound, sparseMatrix : SparseMatrix):
        maxValue = maxBound
        minValue = minBound
        
        numberEntities = findMultipleSameEntitiesHelper(entitiesFound, NUMBER_ENTITY_LABEL)
        numberValues = [] 
        for entity in numberEntities:
            value = entity["value"]
            castedValue, resultType = self.typeController.determineResultType(value)
            numberValues.append(castedValue)

        askForUpperBound = findEntityHelper(entitiesFound, RANGE_UPPER_BOUND_VALUE, by = "value")
        askForMoreThan= findEntityHelper(entitiesFound, RANGE_MORE_THAN_VALUE,  by = "value")

        if len(numberValues) > 1:
            maxValue = max(numberValues)
            minValue = min(numberValues)

            # I add one here, because when the user ask "more than"(lower bound) it means they want more than that year instead of including that year
            # if askForMoreThan:
            #     minYear = minYear+1
        elif len(numberValues) == 1:
            if askForUpperBound:
                minValue = minBound
                maxValue = max(numberValues)
            elif askForMoreThan:
                maxValue = maxBound
                minValue = min(numberValues)
        #Handle the case when no upper bound or lower bound is specified, default to upperbound

        #Making sure the max year and minYear stays in valid range
        maxValue = min(maxValue, maxBound)
        minValue = max(minValue, minBound)
        
        discreteRanges = sparseMatrix.findAllDiscreteRange()
        # print(minBound,maxBound)
        # print(maxValue, minValue)
        # print(discreteRanges)
        rangesToUse = []
        for dRange in discreteRanges:
            if maxValue >= dRange[1] and minValue < dRange[1] and not dRange[0] == None:
                rangesToUse.append(dRange)
        
      
        return rangesToUse

    def aggregateDiscreteRange(self, intent, entities, sparseMatrix : SparseMatrix, isSumming) -> float:
        maxBound, minBound = sparseMatrix.findMaxBoundLowerBoundForDiscreteRange()
        rangeToSumOver = self.findRange(entities, maxBound,  minBound, sparseMatrix)
        
        shouldAddRowStrategy = RangeExactMatchRowStrategy(rangeToSumOver)
        entities = filterEntities(entities, [RANGE_ENTITY_LABEL])
        entitiesUsed = []
        currentResult = []
       
        for r in rangeToSumOver:
            entitiesToCheck = []
            fakeEntity = None
            if r[0]:
                fakeEntity = {
                        "entity": NUMBER_ENTITY_LABEL,
                        "value": str(r[0]) ,
                        "aggregation": "range"
                }
                entitiesToCheck.append(fakeEntity)
            if r[1]:
                fakeEntity = {
                        "entity": NUMBER_ENTITY_LABEL,
                        "value": str(r[1]) ,
                        "aggregation": "range"
                }
                entitiesToCheck.append(fakeEntity)
            answers, intent, entitiesUsedBySearch = self.searchForAnswer(intent, entitiesToCheck, shouldAddRowStrategy, identityFunc)
          
            entitiesUsed = entitiesUsed + entitiesUsedBySearch
            if isSumming:
                if len(answers) == 0:
                    continue
                if len(currentResult) == 0:
                    currentResult.append(answers[0])
                else:
                    currentResult[0]=str(float(currentResult[0]) + float(answers[0]))

                print(currentResult)
            else: 
                currentResult = currentResult + answers
        
        return (currentResult, intent, set(entitiesUsed))



    def aggregatePercentage(self, intent, numerator, entitiesForNumerator, entitiesToCalculateDenominator, shouldAddRowStrategy):
        entitiesUsed = None
        
        answers ,intent, entitiesUsed = self.searchForAnswer(intent, entitiesToCalculateDenominator, shouldAddRowStrategy, identityFunc)
        if len(answers) == 0:
            raise Exception("Answer not found")

        denominator = answers[0]
        percentageCalc = numerator/float(denominator)*100
        percentage = round(percentageCalc, 1)
        percentage = PERCENTAGE_FORMAT.format(value = percentage)
        return (percentage, intent, set(list(entitiesUsed)+ list(entitiesForNumerator)) )
        #return outputFuncForPercentage(percentage, intent, set(list(entitiesUsed)+ list(entitiesForNumerator)) )

    def determineMatrixToSearch(self, intent, entities, year):
        return self.dataManager.determineMatrixToSearch(intent, entities, year)

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


  
