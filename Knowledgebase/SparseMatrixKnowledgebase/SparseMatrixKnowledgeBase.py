

from typing import Dict, Tuple, List
from DataManager.DataManager import DataManager
from DataManager.constants import NUMBER_ENTITY_LABEL, RANGE_ENTITY_LABEL
from Data_Ingestion.SparseMatrix import SparseMatrix
from Knowledgebase.SparseMatrixKnowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.Knowledgebase import KnowledgeBase

from Knowledgebase.Knowledgebase import KnowledgeBase
from Knowledgebase.SparseMatrixKnowledgebase.RangeExactMatchRowStrategy import  RangeExactMatchRowStrategy
from Knowledgebase.DataModels.RangeResultData import RangeResultData
from Knowledgebase.SparseMatrixKnowledgebase.SearchResultType import SearchResultType
from Knowledgebase.SparseMatrixKnowledgebase.TypeController import TypeController

from Knowledgebase.constants import PERCENTAGE_FORMAT
from OutputController.TemplateConverter import TemplateConverter
from actions.constants import AGGREGATION_ENTITY_PERCENTAGE_VALUE, RANGE_LOWER_BOUND_VALUE, RANGE_UPPER_BOUND_VALUE

from actions.entititesHelper import copyEntities, filterEntities, findEntityHelper, findMultipleSameEntitiesHelper
from Parser.RasaCommunicator import RasaCommunicator
from Knowledgebase.DataModels.SearchResult import SearchResult
from actions.entititesHelper import removeDuplicatedEntities
from CustomEntityExtractor.NumberEntityExtractor import NumberEntityExtractor
from CacheLayer.Cache import Cache
from Knowledgebase.DataModels.ChatbotAnswer import ChatbotAnswer
from Knowledgebase.DataModels.MultiFeedbackLabel import MultiFeedbackLabel
import aiohttp
import asyncio

class SparseMatrixKnowledgeBase(KnowledgeBase):
    def __init__(self, dataManager):
        self.dataManager : DataManager = dataManager
     
        self.typeController = TypeController()
        self.templateConverter : TemplateConverter = TemplateConverter()

        self.rasaCommunicator = RasaCommunicator()
        self.numberEntityExtractor = NumberEntityExtractor()

        self.source = "SparseMatrixKnowledgebase"

    

   
    async def searchForAnswer(self, question, intent, entitiesExtracted, startYear, endYear, completeSentence=True) ->Tuple[List[ChatbotAnswer], bool]:         
        # print("BEGAN SEARCHING")
        shouldAddRowStrategy = DefaultShouldAddRowStrategy()
        answers = []
        sparseMatrixToSearch : SparseMatrix
        sparseMatricesToSearch = await self.determineMatrixToSearch(intent, entitiesExtracted, startYear, endYear)
        if sparseMatricesToSearch is None or len(sparseMatricesToSearch) == 0:
                raise Exception("No valid sparse matrix found for given intent and entities", intent, entitiesExtracted)
    
        # print(entitiesExtracted)
        #Use the first sparse matrix.
        # 
        # for sparseMatrixToSearch in sparseMatricesToSearch:
        sparseMatrixToSearch : SparseMatrix = sparseMatricesToSearch[0]
        isOperationAllowed = sparseMatrixToSearch.isAnyOperationAllowed()
        template = sparseMatrixToSearch.findTemplate()

        if(not isOperationAllowed and template == ""):
            return ([], True)
    
        isRangeAllowed = sparseMatrixToSearch.isRangeOperationAllowed()
        hasRangeEntity = findEntityHelper(entitiesExtracted, RANGE_ENTITY_LABEL) 
        isSumAllowed = sparseMatrixToSearch.isSumOperationAllowed()

        isPercentageAllowed = sparseMatrixToSearch.isPercentageOperationAllowed()
        
        percentageEntityDetected = findEntityHelper(entitiesExtracted, AGGREGATION_ENTITY_PERCENTAGE_VALUE, by="value") 
        searchResults = []
    
        if isRangeAllowed and hasRangeEntity:
            rangeResultData : RangeResultData =  self.aggregateDiscreteRange(entitiesExtracted, sparseMatrixToSearch, isSumAllowed)
            filteredEntities = filterEntities(entitiesExtracted, [RANGE_ENTITY_LABEL, NUMBER_ENTITY_LABEL])
        
            searchResults : List[SearchResult] = rangeResultData.answers
            for searchResult in searchResults:
             
                searchResult.addEntities(filteredEntities)
        else:
            # print("REGULAR SEARCH")
            searchResults : List[SearchResult] = sparseMatrixToSearch.searchOnSparseMatrix(entitiesExtracted, shouldAddRowStrategy, isSumAllowed)


        if isPercentageAllowed and percentageEntityDetected:
            percentages = await self.calculatePercentages(searchResults, sparseMatrixToSearch,  percentageEntityDetected, startYear, endYear)
            print("GOT PERCENTAGE", percentages)
            searchResults = percentages

        await self.getAllEntityForRealQuestionFoundForAnswer(searchResults)

        # also get the documentation of change 
        documentationOfChange = sparseMatrixToSearch.getDocumentationOfChange()
        answers = answers + self.constructOutput(searchResults, intent,  template, completeSentence) 

        shouldContinue = True
        if len(answers) > 0:
            shouldContinue = False
            if not documentationOfChange == None:
                answers.append(documentationOfChange)
        
        # print("OKAY I AM GONNA RETURN", answers)
        return (answers, shouldContinue)


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
    async def calculatePercentages(self, searchResults : List[SearchResult], sparseMatrix : SparseMatrix, percentageEntityDetected : Dict[str, str], startYear, endYear) -> List[str]:
        print("CALCULATING PERCENTAGE")
        denominatorQuestion = sparseMatrix.findDenominatorQuestion()
        percentageSearchInSelf = sparseMatrix.shouldSearchInSelfForPercentage()
        response = {}
        async with aiohttp.ClientSession() as session:
            response = await self.rasaCommunicator.parseMessage(denominatorQuestion, session)
     
        entitiesFromDenominatorQuestion = response["entities"]
        intentObj = response["intent"]
        intent = intentObj["name"]
        percentages = []
        print("GIVEN SEARCH RESULTS")
        print(searchResults)
        for searchResult in searchResults:
            print("NUMERATOR")
            print(searchResult.answer)
            entitiesUsedForThisSearchResult = searchResult.getEntitiesUsed()
            entitiesForDenominator = entitiesFromDenominatorQuestion
            if percentageSearchInSelf:
                searchResultEntities =  filterEntities(entitiesUsedForThisSearchResult, [RANGE_ENTITY_LABEL])
                entitiesForDenominator =  entitiesFromDenominatorQuestion + searchResultEntities
                

            print(entitiesForDenominator)
            print(intent)

            chatbotAnswers, shouldContinue = await self.searchForAnswer(denominatorQuestion, intent, entitiesForDenominator,startYear, endYear, completeSentence=False )
            
         
            print("DENOMINATOR")
            print(chatbotAnswers)
            # if len(chatbotAnswers) == 0:
            #     continue
            
            print("DENOMINATOR VALUE")
            denominator = chatbotAnswers[0]
            print(denominator.answer)
            
            # try:
                # numerator = float(searchResult.answer)
            numerator, type = self.typeController.determineResultType(searchResult.answer)
            denominator, type = self.typeController.determineResultType(denominator.answer)
            percentageCalc = (numerator/denominator)*100
            percentage = round(percentageCalc, 1)
            percentage = PERCENTAGE_FORMAT.format(value = percentage)
            allEntityUsedAndPercentage = entitiesUsedForThisSearchResult + [percentageEntityDetected]
            percentageSearchResult = SearchResult(percentage, allEntityUsedAndPercentage, SearchResultType.PERCENTAGE, searchResult.realQuestion)
            percentages.append(percentageSearchResult)
            # except Exception as e:
            #     print("EXCEPTION OCCURED WHILE CALCULATING PERCENTAGE", e.__dict__)
            #     continue
        # for t in percentages:
        #     print(t.entities)
        return percentages
        

    def getAvailableOptions(self, intent, startYear, endYear) -> Dict[str, List[str]]:
        return self.dataManager.getAvailableOptions(self,startYear, endYear)

    async def determineMatrixToSearch(self, intent, entities, startYear, endYear):
        return await self.dataManager.determineMatrixToSearch(intent, entities, startYear, endYear)

    def constructOutput(self, searchResults : List[SearchResult], intent, template, completeSentence):
        chatbotAnswers = []
        if completeSentence:
            if searchResults is None or len(searchResults) == 0: 
                    return []
            if template == "" or template == "nan":
                print("NO Template")
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

            allAnswers = sentences + stringSentence
            
            chatbotAnswers : List[ChatbotAnswer] = []
            for answer in allAnswers:
                chatbotAnswer = ChatbotAnswer(answer=answer, source = self.source)
                chatbotAnswers.append(chatbotAnswer)
        else:
            for result in searchResults:
                chatbotAnswer =  ChatbotAnswer(answer=result.answer, source = self.source)
                chatbotAnswers.append(chatbotAnswer)

        return chatbotAnswers
        
       
  
    def findRange(self, entitiesFound, maxBound, minBound, sparseMatrix : SparseMatrix) -> List[Tuple[float, float]]:
        """
        This function will use the entities found from the user query, to determine whether if the user is asking
        for lowerbound(greater than some value), upperbound(within some value) or both(a range) and determine the discrete ranges 
        of the sparse matrix that intersect with the user specified range.

        :param entitiesFound: Entities found from user query
        :param maxBound: maxBound of the Sparse Matrix
        :param minBound: minBound of the Sparse Matrix
        :param sparseMatrix: sparse matrix currently being searched on
        
        """
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
        print("INTERVAL TO CHECK")
        print(intervalToCheck)
        print(discreteRanges)

        for dRange in discreteRanges:
            if self.doesIntervalOverlap(intervalToCheck, dRange):
                rangesToUse.append(dRange)
    
        return rangesToUse
    
        
    def doesIntervalOverlap(self,a, b):
        if not a[0] >= b[1] and not a[1] <= b[0]:
            return True
        else:
            return False

    def aggregateDiscreteRange(self, entities, sparseMatrix : SparseMatrix, isSumming : bool) -> RangeResultData:
        """
        This function will aggregate over discrete ranges based on entities detected from user and either sum them up or append them 
        as seperate answres.
        :param entities: entities detected from user query
        :param sparseMatrix: sparse matrix being searched
        :param isSumming: Whether to add up the answer or append as seperate answers.
        """
        maxBound, minBound = sparseMatrix.findMaxBoundLowerBoundForDiscreteRange()
        rangesToSumOver = self.findRange(entities, maxBound,  minBound, sparseMatrix)
        print(maxBound, minBound)
        print("RANGE TO SUM OVER")
        print(rangesToSumOver)
        shouldAddRowStrategy = RangeExactMatchRowStrategy()
        entities = filterEntities(entities, [RANGE_ENTITY_LABEL, NUMBER_ENTITY_LABEL])
        answerPointer : SearchResult = None

        foundAnswers : List[SearchResult] = []
        rangeResultData = RangeResultData()
       
        minRange = float('inf')
        maxRange = float('-inf')
        for r in rangesToSumOver:
            entitiesToCheck = entities.copy()
            fakeEntity = None

            minRange = min(minRange, r[0])
            maxRange = max(maxRange, r[1])
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

            print("ENTITIES TO CHECK")
            print(entitiesToCheck)

            searchResults : List[SearchResult] = sparseMatrix.searchOnSparseMatrix(entitiesToCheck, shouldAddRowStrategy,isSumming)
            if len(searchResults) == 0:
                continue
            # On each iteration, we expect to only get one answer from search
            searchResult = searchResults[0]
            print(searchResult.answer)
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
        return rangeResultData

    
  
    def train(self, trainingLabels : List[MultiFeedbackLabel], callback) -> bool:
        callback(True)
        return True
    
    async def dataUploaded(self, dataName, startYear = None, endYear = None ):
        pass

    def dataDeleted(self, dataName):
        pass