

from typing import Dict, Tuple, List
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
from Knowledgebase.DataModels.RangeResultData import RangeResultData
from Knowledgebase.SearchResultType import SearchResultType
from Knowledgebase.TypeController import TypeController

from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController.TemplateConverter import TemplateConverter
from OutputController.output import  constructSentence, identityFunc, outputFuncForPercentage
from actions.constants import AGGREGATION_ENTITY_PERCENTAGE_VALUE, RANGE_LOWER_BOUND_VALUE, RANGE_UPPER_BOUND_VALUE

from actions.entititesHelper import copyEntities, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper
from Parser.RasaCommunicator import RasaCommunicator
from Knowledgebase.DataModels.SearchResult import SearchResult
from tests.testUtils import createEntityObjHelper
import aiohttp
import asyncio

class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
        self.typeController = TypeController()
        self.templateConverter : TemplateConverter = TemplateConverter()
        self.year = self.dataManager.getMostRecentYearRange()[0]
        self.rasaCommunicator = RasaCommunicator()

    
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

        #Entities used corresponding to each search result
        entitiesUsedForEachResult : List[List[Dict[str, str]]]= []

        # print("ENTITIES EXTRACtED")
        # print("TAOAOJFOAJFSOSJFJSAFOJFO_______________")
        # print(entitiesExtracted)
        print(sparseMatrixToSearch.subSectionName)
        if isRangeAllowed and hasRangeEntity:
            print("RANGE")
            rangeResultData : RangeResultData =  self.aggregateDiscreteRange(entitiesExtracted, sparseMatrixToSearch, isSumAllowed)
            filteredEntities = filterEntities(entitiesExtracted, [RANGE_ENTITY_LABEL, NUMBER_ENTITY_LABEL])
           
            searchResults = rangeResultData.answers
            for entities in rangeResultData.entitiesUsedForAnswer:
                entitiesUsedForEachResult.append(entities+filteredEntities)

            # print("GOT IT")
            # print(entitiesUsedForEachResult)

        else:

            searchResults : List[SearchResult] = sparseMatrixToSearch.searchOnSparseMatrix(entitiesExtracted, shouldAddRowStrategy, isSumAllowed)
            # entitiesUsedForEachResult = [entitiesUsed]*len(searchResults)

        # if isPercentageAllowed and hasPercentageEntity:
        #     percentages = self.calculatePercentages(searchResults, sparseMatrixToSearch)
        #     if percentages == None or len(percentages) == 0:
        #         return outputFunc(searchResults, intent, template)
        #     else:
                # return outputFunc(percentages, intent, template)
        
        print("REGULAR OUTPUT")
        return outputFunc(searchResults, intent,  template)

    

    
    # STILL WORK IN PROGRESS
    async def calculatePercentages(self, searchResults, entitiesForEachResult : List[List[Dict[str, str]]], sparseMatrix : SparseMatrix) -> List[str]:
        shouldAddRowStrategy = DefaultShouldAddRowStrategy()
        denominatorQuestion = sparseMatrix.findDenominatorQuestion()
        percentageSearchInSelf = sparseMatrix.shouldSearchInSelfForPercentage()
        async with aiohttp.ClientSession() as session:
            response = await self.rasaCommunicator.parseMessage(denominatorQuestion, session)
            entitiesFromDenominatorQuestion = response["entities"]

            percentages = []
            for searchResult, entitiesUsed in zip(searchResults, entitiesForEachResult):
                entitiesForDenominator = entitiesFromDenominatorQuestion
                if percentageSearchInSelf:
                    entitiesForDenominator =  entitiesFromDenominatorQuestion + entitiesUsed
                answers, entitiesUsed = sparseMatrix.searchOnSparseMatrix(entitiesForDenominator, shouldAddRowStrategy, True)
                if len(answers) == 0:
                    return []

                denominator = answers[0]
                try:
                    numerator = searchResult
                    percentageCalc = numerator/float(denominator)*100
                    percentage = round(percentageCalc, 1)
                    percentage = PERCENTAGE_FORMAT.format(value = percentage)
                    percentages.append(percentage)
                except:
                    continue

            return percentages
        
        
    def getAvailableOptions(self, key):
        pass

    def determineMatrixToSearch(self, intent, entities, year):
        return self.dataManager.determineMatrixToSearch(intent, entities, year)

    def constructOutput(self, searchResults : List[SearchResult], intent, template):
       #return searchResult
       print("CONSTRUCTING OUTPUT")
       if searchResults is None or len(searchResults) == 0: 
            return ["Sorry, I couldn't find any answer to your question"]
        
       if template == "" or template == "nan":
            return map(lambda x: x.answer , searchResults)

       constructSentenceFor = []
       stringSentence = []
       for result in searchResults:
            if result.type== SearchResultType.STRING:
                stringSentence.append(result.answer)
            else:
                constructSentenceFor.append(result)

      
       sentences = self.templateConverter.constructOutput(constructSentenceFor, template)
       
       return sentences + stringSentence
       #return constructSentence(searchResult, intent, entitiesUsed)

  
    def findRange(self, entitiesFound, maxBound, minBound, sparseMatrix : SparseMatrix):
        maxValue = maxBound
        minValue = minBound
        # print("MIN BOUND MAX BOUND")
        # print(minBound, maxBound)
    
        numberEntities = findMultipleSameEntitiesHelper(entitiesFound, NUMBER_ENTITY_LABEL)
        numberValues = [] 
        # print(numberEntities)
        for entity in numberEntities:
            value = entity["value"]
            castedValue, resultType = self.typeController.determineResultType(value)
            numberValues.append(castedValue)

        askForUpperBound = findEntityHelper(entitiesFound, RANGE_UPPER_BOUND_VALUE, by = "value")
        askForLowerBound= findEntityHelper(entitiesFound, RANGE_LOWER_BOUND_VALUE,  by = "value")

        if len(numberValues) > 1:
            maxValue = max(numberValues)
            minValue = min(numberValues)
          
        elif len(numberValues) == 1:
            if askForUpperBound or not (askForUpperBound or askForLowerBound ):
                minValue = float('-inf')
                maxValue = max(numberValues)
              
            elif askForLowerBound:
                maxValue = float('inf')
                minValue = min(numberValues)
               

        elif len(numberEntities) == 0:
            minValue = float('-inf')
            maxValue = float('inf')
            
        discreteRanges = sparseMatrix.findAllDiscreteRange()
        # print("DISCRETE RANGES")
        # print(discreteRanges)
        # print(minBound,maxBound)
        rangesToUse = []
        intervalToCheck = [minValue, maxValue]
        
        # print("INTERVAL TO CHECK")
        # print(intervalToCheck)
        for dRange in discreteRanges:
            if self.doesIntervalOverlap(intervalToCheck, dRange):
                rangesToUse.append(dRange)
        # print("MIN VALUE MAX VALUE")
        # print(minValue, maxValue)
        # print("RANGE TO USE")
        # print(rangesToUse)
        return rangesToUse
    
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
        # a = self.convertNoneToInfinity(a)
        # b = self.convertNoneToInfinity(b)
        if not a[0] >= b[1] and not a[1] <= b[0]:
            return True
        else:
            return False

    def aggregateDiscreteRange(self, entities, sparseMatrix : SparseMatrix, isSumming):
        maxBound, minBound = sparseMatrix.findMaxBoundLowerBoundForDiscreteRange()
        rangesToSumOver = self.findRange(entities, maxBound,  minBound, sparseMatrix)
        print("RANGE TO SUM OVER")
        print(rangesToSumOver)

        shouldAddRowStrategy = RangeExactMatchRowStrategy()
        entities = filterEntities(entities, [RANGE_ENTITY_LABEL])
        entitiesUsed = []
        answerPointer : SearchResult = None

        foundAnswers : List[SearchResult] = []
        rangeResultData = RangeResultData()
        # print("RANGE TO SUM")
        # print(rangesToSumOver)

        minRange = float('-inf')
        maxRange = float('inf')
        for r in rangesToSumOver:
            entitiesToCheck = []
            fakeEntity = None

            minRange = max(minRange, r[0])
            maxRange = min(maxRange, r[1])
            if not r[0] == float('inf') and not r[0] == float('-inf')  :
                fakeEntity = {
                        "entity": NUMBER_ENTITY_LABEL,
                        "value": str(r[0]) ,
                }
                entitiesToCheck.append(fakeEntity)

            if not r[1] == float('inf') and not r[1] == float('-inf') :
                fakeEntity = {
                        "entity": NUMBER_ENTITY_LABEL,
                        "value": str(r[1]) ,
                }
                entitiesToCheck.append(fakeEntity)

            searchResults : List[SearchResult] = sparseMatrix.searchOnSparseMatrix(entitiesToCheck, shouldAddRowStrategy,isSumming)
            if len(searchResults) == 0:
                continue

            # On each iteration, we expect to only get one answer from search
            searchResult = searchResults[0]
            # entitiesUsed.append(searchResult.entitiesUsed)

            answerPointer = sparseMatrix.addSearchResult(answerPointer, searchResult, foundAnswers, isSumming)
        # Construct the range entity:   
        rangeToCreateEntityFor = rangesToSumOver
        if isSumming:
            rangeToCreateEntityFor = [[minRange, maxRange]]
        rangeResultData.createFinalResultAndEntities(rangeToCreateEntityFor, foundAnswers)
        # entitiesToUse = self.constructRangeEntityHelper(intention, numbersUsed)
        return rangeResultData

    

