
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
from Knowledgebase.RangeResultData import RangeResultData
from Knowledgebase.SearchResultType import SearchResultType
from Knowledgebase.TypeController import TypeController

from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController.TemplateConverter import TemplateConverter
from OutputController.output import  constructSentence, identityFunc, outputFuncForPercentage
from actions.constants import AGGREGATION_ENTITY_PERCENTAGE_VALUE, RANGE_LOWER_BOUND_VALUE, RANGE_UPPER_BOUND_VALUE

from actions.entititesHelper import copyEntities, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper
from tests.testUtils import createEntityObjHelper


class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
        self.typeController = TypeController()
        self.templateConverter : TemplateConverter = TemplateConverter()
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
        # print("BEGAN SEARCHING")
        sparseMatrixToSearch : SparseMatrix; startYear : str; endYear : str 
        sparseMatrixToSearch, startYear, endYear = self.determineMatrixToSearch(intent, entitiesExtracted, self.year)
        
        if sparseMatrixToSearch is None:
            raise Exception("No valid sparse matrix found for given intent and entities", intent, entitiesExtracted)

        isRangeAllowed = sparseMatrixToSearch.isRangeOperationAllowed()
        hasRangeEntity = findEntityHelper(entitiesExtracted, RANGE_ENTITY_LABEL)
        isSumAllowed = sparseMatrixToSearch.isSumOperationAllowed()

        isPercentageAllowed = sparseMatrixToSearch.isPercentageOperationAllowed()
        hasPercentageEntity = findEntityHelper(entitiesExtracted, AGGREGATION_ENTITY_PERCENTAGE_VALUE)
        template = sparseMatrixToSearch.findTemplate()
        searchResults = []
        entitiesUsed = []
        if isRangeAllowed and hasRangeEntity:
            rangeResultData : RangeResultData =  self.aggregateDiscreteRange(intent, entitiesExtracted, sparseMatrixToSearch, isSumAllowed)
            filteredEntities = filterEntities(entitiesExtracted, RANGE_ENTITY_LABEL)
            entitiesUsed = entitiesUsed + filteredEntities
            sentences = []
            for answer, entities in zip(rangeResultData.answers, rangeResultData.entitiesUsedForAnswer):
                sentence = outputFunc([answer], intent, entities, template)
                sentences = sentences +sentence
                
            return sentences
        elif isPercentageAllowed and hasPercentageEntity:
            return outputFunc(searchResults, intent, entitiesUsed, template)
        else:
            print("PERFORMING REGULAR SEARCH")
            print(sparseMatrixToSearch.sparseMatrixDf)
            searchResults, entitiesUsed = sparseMatrixToSearch.searchOnSparseMatrix(entitiesExtracted, shouldAddRowStrategy, isSumAllowed)
            print(searchResults)
            return outputFunc(searchResults, intent, entitiesUsed, template)



    def constructOutput(self, searchResults, intent, entitiesUsed, template):
       #return searchResult
       if searchResults is None or len(searchResults) == 0: 
            return ["Sorry, I couldn't find any answer to your question"]
        
       if template == "" or template == "nan":
            return searchResults

       sentences = self.templateConverter.constructOutput(searchResults,  entitiesUsed, template)
       return sentences
       #return constructSentence(searchResult, intent, entitiesUsed)

  
    def findRange(self, entitiesFound, maxBound, minBound, sparseMatrix : SparseMatrix):
        maxValue = maxBound
        minValue = minBound
        intention = ""
        numberEntities = findMultipleSameEntitiesHelper(entitiesFound, NUMBER_ENTITY_LABEL)
        numberValues = [] 
        for entity in numberEntities:
            value = entity["value"]
            castedValue, resultType = self.typeController.determineResultType(value)
            numberValues.append(castedValue)

        askForUpperBound = findEntityHelper(entitiesFound, RANGE_UPPER_BOUND_VALUE, by = "value")
        askForMoreThan= findEntityHelper(entitiesFound, RANGE_LOWER_BOUND_VALUE,  by = "value")

        if len(numberValues) > 1:
            maxValue = max(numberValues)
            minValue = min(numberValues)
            intention = "between"

        elif len(numberValues) == 1:
            if askForUpperBound or not (askForUpperBound or askForMoreThan ):
                minValue = float('-inf')
                maxValue = max(numberValues)
                intention = "upperBound"
            elif askForMoreThan:
                maxValue = float('inf')
                minValue = min(numberValues)
                intention = "lowerBound"

        elif len(numberEntities) == 0:
            minValue = float('-inf')
            maxValue = float('inf')
            intention = "between"
            
        discreteRanges = sparseMatrix.findAllDiscreteRange()
        # print(minBound,maxBound)
        rangesToUse = []
        intervalToCheck = [minValue, maxValue]
        for dRange in discreteRanges:
            if self.doesIntervalOverlap(intervalToCheck, dRange):
                rangesToUse.append(dRange)
  
        return (rangesToUse, intention)
    
    def convertNoneToInfinity(self,a):
        newRes = []
        if a[0] and a[1]:
            return a

        if a[0] == None:
            newRes.append(float('-inf'))
            newRes.append(a[1])
        if a[1] == None:
            newRes.append(a[0])
            newRes.append(float('inf'))
        return newRes
        
    def doesIntervalOverlap(self,a, b):
        a = self.convertNoneToInfinity(a)
        b = self.convertNoneToInfinity(b)
        if not a[0] >= b[1] and not a[1] <= b[0]:
            return True
        else:
            return False

    def aggregateDiscreteRange(self, intent, entities, sparseMatrix : SparseMatrix, isSumming):
        maxBound, minBound = sparseMatrix.findMaxBoundLowerBoundForDiscreteRange()
        rangesToSumOver, intention  = self.findRange(entities, maxBound,  minBound, sparseMatrix)
        shouldAddRowStrategy = RangeExactMatchRowStrategy()
        entities = filterEntities(entities, [RANGE_ENTITY_LABEL])
        entitiesUsed = []
        answerPointer = None

        foundAnswers = []
        rangeResultData = RangeResultData()
        for r in rangesToSumOver:
            entitiesToCheck = []
            fakeEntity = None
            if r[0]:
                fakeEntity = {
                        "entity": NUMBER_ENTITY_LABEL,
                        "value": str(r[0]) ,
                }
                entitiesToCheck.append(fakeEntity)

            if r[1]:
                fakeEntity = {
                        "entity": NUMBER_ENTITY_LABEL,
                        "value": str(r[1]) ,
                }
                entitiesToCheck.append(fakeEntity)
            
            answers, intent, entitiesUsedBySearch = self.searchForAnswer(intent, entitiesToCheck, shouldAddRowStrategy, identityFunc)
            if len(answers) == 0:
                continue

            entitiesUsed.append(entitiesUsedBySearch)

            # On each iteration, we expect to only get one answer from search
            answerPointer = sparseMatrix.addSearchResult(answerPointer, answers[0], foundAnswers, isSumming)
        # Construct the range entity:   
        rangeResultData.createFinalResultAndEntities(intention, isSumming, foundAnswers, entitiesUsed)
        # entitiesToUse = self.constructRangeEntityHelper(intention, numbersUsed)
        return rangeResultData

    


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



