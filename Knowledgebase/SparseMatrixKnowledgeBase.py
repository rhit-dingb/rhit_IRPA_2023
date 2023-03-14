

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
from actions.entititesHelper import removeDuplicatedEntities
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from Knowledgebase.FuzzyShouldAddRowStrategy import FuzzyShouldAddRowStrategy
from CacheLayer.Cache import Cache
from tests.testUtils import createEntityObjHelper
import aiohttp
import asyncio

class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
     
        self.typeController = TypeController()
        self.templateConverter : TemplateConverter = TemplateConverter()

        self.rasaCommunicator = RasaCommunicator()
        self.numberEntityExtractor = NumberEntityExtractor()

    

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
    async def searchForAnswer(self, intent, entitiesExtracted, shouldAddRowStrategy, outputFunc, startYear, endYear):
        # print("BEGAN SEARCHING")
        answers = []
        sparseMatrixToSearch : SparseMatrix
        sparseMatricesToSearch = await self.determineMatrixToSearch(intent, entitiesExtracted, startYear, endYear)
        if sparseMatricesToSearch is None or len(sparseMatricesToSearch) == 0:
                raise Exception("No valid sparse matrix found for given intent and entities", intent, entitiesExtracted)

        #Use the first sparse matrix.
        # 
        # for sparseMatrixToSearch in sparseMatricesToSearch:
        sparseMatrixToSearch : SparseMatrix = sparseMatricesToSearch[0]
        print(len(sparseMatricesToSearch))
        print("SELECTED")
        print(sparseMatrixToSearch.subSectionName)
        isOperationAllowed = sparseMatrixToSearch.isAnyOperationAllowed()
    
        isRangeAllowed = sparseMatrixToSearch.isRangeOperationAllowed()
        hasRangeEntity = findEntityHelper(entitiesExtracted, RANGE_ENTITY_LABEL)
        isSumAllowed = sparseMatrixToSearch.isSumOperationAllowed()

        isPercentageAllowed = sparseMatrixToSearch.isPercentageOperationAllowed()
        percentageEntityDetected = findEntityHelper(entitiesExtracted, AGGREGATION_ENTITY_PERCENTAGE_VALUE, by="value")
        template = sparseMatrixToSearch.findTemplate()
        searchResults = []
    
        if isRangeAllowed and hasRangeEntity:
            rangeResultData : RangeResultData =  self.aggregateDiscreteRange(entitiesExtracted, sparseMatrixToSearch, isSumAllowed)
            filteredEntities = filterEntities(entitiesExtracted, [RANGE_ENTITY_LABEL, NUMBER_ENTITY_LABEL])
            searchResults : List[SearchResult] = rangeResultData.answers
            for searchResult in searchResults:
                searchResult.addEntities(filteredEntities)
        else:
            searchResults : List[SearchResult] = sparseMatrixToSearch.searchOnSparseMatrix(entitiesExtracted, shouldAddRowStrategy, isSumAllowed)
        if isPercentageAllowed and percentageEntityDetected:
            percentages = await self.calculatePercentages(searchResults, sparseMatrixToSearch,  percentageEntityDetected)
            # print("GOT VALUE ", percentages)
            if not percentages == None and len(percentages) > 0:
                searchResults = percentages
        await self.getAllEntityForRealQuestionFoundForAnswer(searchResults)

        # also get the documentation of change 
        documentationOfChange = sparseMatrixToSearch.getDocumentationOfChange()
        answers = answers + outputFunc(searchResults, intent,  template) 
        if len(answers) > 0 and not documentationOfChange == None:
            answers.append(documentationOfChange)
        
        return answers


    async def getAllEntityForRealQuestionFoundForAnswer(self, searchResults : List[SearchResult]):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for searchResult in searchResults:
                realQuestion = searchResult.realQuestion
                task = asyncio.create_task(self.rasaCommunicator.parseMessage(realQuestion, session=session))
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
          
            for searchResult, response in zip(searchResults, responses):
                #Would probably be better if we put this number entity extractor in the config pipeline, so we don't need to call it everytime we want to get entities.
                entities = response["entities"]
                numberEntities = self.numberEntityExtractor.extractEntities(searchResult.realQuestion)
                entities = entities+numberEntities
                entities = removeDuplicatedEntities(entities)
                searchResult.setEntitiesForRealQuestion(entities)
           
        
    
    # STILL WORK IN PROGRESS
    async def calculatePercentages(self, searchResults : List[SearchResult], sparseMatrix : SparseMatrix, percentageEntityDetected : Dict[str, str]) -> List[str]:
        shouldAddRowStrategy = DefaultShouldAddRowStrategy()
        denominatorQuestion = sparseMatrix.findDenominatorQuestion()
        percentageSearchInSelf = sparseMatrix.shouldSearchInSelfForPercentage()
        async with aiohttp.ClientSession() as session:
            response = await self.rasaCommunicator.parseMessage(denominatorQuestion, session)
            entitiesFromDenominatorQuestion = response["entities"]

            percentages = []
            
            for searchResult in searchResults:
                entitiesUsedForThisSearchResult = searchResult.getEntitiesUsed()
                entitiesForDenominator = entitiesFromDenominatorQuestion
                if percentageSearchInSelf:
                    entitiesForDenominator =  entitiesFromDenominatorQuestion + entitiesUsedForThisSearchResult
                
                searchResults = sparseMatrix.searchOnSparseMatrix(entitiesForDenominator, shouldAddRowStrategy, True)
                if len(searchResults) == 0:
                    return []

                denominator = searchResults[0]
                # try:
                numerator = float(searchResult.answer)
                percentageCalc = numerator/float(denominator.answer)*100
                percentage = round(percentageCalc, 1)
                percentage = PERCENTAGE_FORMAT.format(value = percentage)
                allEntityUsedAndPercentage = entitiesUsedForThisSearchResult + [percentageEntityDetected]
             
                percentageSearchResult = SearchResult(percentage, allEntityUsedAndPercentage, SearchResultType.PERCENTAGE, searchResult.realQuestion)
                percentages.append(percentageSearchResult)
                # except:
                #     continue

            return percentages
        

    def getAvailableOptions(self, intent, startYear, endYear) -> Dict[str, List[str]]:
        return self.dataManager.getAvailableOptions(self,startYear, endYear)

    async def determineMatrixToSearch(self, intent, entities, startYear, endYear):
        return await self.dataManager.determineMatrixToSearch(intent, entities, startYear, endYear)

    def constructOutput(self, searchResults : List[SearchResult], intent, template):
       #return searchResult
       if searchResults is None or len(searchResults) == 0: 
            return []
       if template == "" or template == "nan":
            return list(map(lambda x: x.answer , searchResults))

       constructSentenceFor = []
       stringSentence = []
       for result in searchResults:
            if result.answer.lower() == "n/a":
                constructSentenceFor.append(result)
                
            elif result.type == SearchResultType.STRING:
                stringSentence.append(str(result.answer))
            else:
                constructSentenceFor.append(result)
       sentences = self.templateConverter.constructOutput(constructSentenceFor, template)
       return sentences + stringSentence
       
  
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
    
        rangesToUse = []
        intervalToCheck = [minValue, maxValue]
        # print("INTERVAL TO CHECK")
        # print(intervalToCheck)
        for dRange in discreteRanges:
            if self.doesIntervalOverlap(intervalToCheck, dRange):
                rangesToUse.append(dRange)
    
        return rangesToUse
    
        
    def doesIntervalOverlap(self,a, b):
        if not a[0] >= b[1] and not a[1] <= b[0]:
            return True
        else:
            return False

    def aggregateDiscreteRange(self, entities, sparseMatrix : SparseMatrix, isSumming):
        maxBound, minBound = sparseMatrix.findMaxBoundLowerBoundForDiscreteRange()
        rangesToSumOver = self.findRange(entities, maxBound,  minBound, sparseMatrix)
        print(maxBound, minBound)
        print("RANGE TO SUM OVER")
        print(rangesToSumOver)

        shouldAddRowStrategy = RangeExactMatchRowStrategy()
        entities = filterEntities(entities, [RANGE_ENTITY_LABEL])
        answerPointer : SearchResult = None

        foundAnswers : List[SearchResult] = []
        rangeResultData = RangeResultData()
       
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
            if answerPointer == None:
                answerPointer = searchResult
                foundAnswers.append(searchResult)
            else:
                answerPointer = sparseMatrix.addSearchResult(answerPointer, searchResult, foundAnswers, isSumming)

        # Construct the range entity:   
        rangeToCreateEntityFor = rangesToSumOver
        if isSumming:
            rangeToCreateEntityFor = [[minRange, maxRange]]
        rangeResultData.createFinalResultAndEntities(rangeToCreateEntityFor, foundAnswers)
        # entitiesToUse = self.constructRangeEntityHelper(intention, numbersUsed)
        return rangeResultData

    

