"""
Internal data model representing a sparse matrix
"""

import json
from typing import List, Tuple
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.SearchResultType import SearchResultType

from Knowledgebase.TypeController import TypeController
from actions.entititesHelper import createEntityObj
import Data_Ingestion.constants as constants
import pandas as pd

from actions.constants import RANGE_LOWER_BOUND_VALUE
from Knowledgebase.DataModels.SearchResult import SearchResult

class SparseMatrix():
    def __init__(self, subSectionName, sparseMatrixDf, questions=[]):
        self.subSectionName = subSectionName
        self.sparseMatrixDf : pd.DataFrame  = sparseMatrixDf
        self.typeController = TypeController()
        self.questions = []
        if len(questions) == self.sparseMatrixDf.shape[0]:
            self.questions = questions

    def getColumn(self):
        return self.sparseMatrixDf.loc[0].index
        
    # def getColumnWithOneForEachRow(self):
    #     columnList : List[List[str]]
    #     for row in self:
    #         columnVals = []
    #         for column in row.index:
    #             if row[column] == 1:
    #                 columnVals.append(column)
            
    #         columnList.append(columnVals)
    #     return columnList

    def __iter__(self):
        for i in range(self.sparseMatrixDf.shape[0]):
            row = self.sparseMatrixDf.loc[i]
            yield row

    def rowsToJson(self):
        jsonRows = []
        for row, question in zip(self, self.questions):
           
            rowJson = row.to_json()
            jsonDict = json.loads(rowJson)
            jsonDict["question"] = question
            jsonRows.append(jsonDict)
        return jsonRows

    def getSparseMatrixDf(self):
        return self.sparseMatrixDf

    """
    This function determine the number of entities extracted that matches the columns of the sparse matrix
    """

    def determineEntityMatchToColumnCount(self, entities) -> int:
        return self.determineMatchCountHelper(entities, self.sparseMatrixDf.columns)

    
    # #This function determines how many elements in the first array is in the second array.
    def determineMatchCountHelper(self, entities: List[str], columns: List[str]):
        entitiesMatchCount = 0
        for entity in entities:
            if entity in columns:
                entitiesMatchCount = entitiesMatchCount + 1
        # print("ENTITY MATCH COUNT FOR")
        # print(self.subSectionName)
        # print(entitiesMatchCount)
        return entitiesMatchCount


    def findMaxBoundLowerBoundForDiscreteRange(self):
        ranges = self.findAllDiscreteRange()
        maxBound = None
        minBound = None
        for r in ranges:
            upperBound = r[1]
            lowerBound = r[0]
            if upperBound and (maxBound is None or upperBound>maxBound):
                maxBound = upperBound

            if lowerBound and (minBound is None or lowerBound<minBound):
                minBound = lowerBound

        return (maxBound, minBound)

    
    def findAllDiscreteRange(self) :
        discreteRanges = []
        for i in range(self.sparseMatrixDf.shape[0]):
            row = self.sparseMatrixDf.loc[i]
            rangeFound = self.findRangeForRow(row)
            if len(rangeFound) == 2:
                if not rangeFound in discreteRanges:
                    discreteRanges.append(rangeFound)

        return discreteRanges

    def findRangeForRow(self,row):
        discreteRange = []
        for columnLabel in row.index:
            castedValue, resultType = self.typeController.determineResultType(columnLabel)
            if (resultType == SearchResultType.NUMBER or resultType == SearchResultType.FLOAT) and row[columnLabel] == 1:
                discreteRange.append(castedValue)
        discreteRange.sort()
        if len(discreteRange) == 1:
            if self.isColumnMarkedForRow(row, RANGE_LOWER_BOUND_VALUE):
                discreteRange.append(float('inf'))
            else:
                discreteRange.insert(0,  float('-inf'))

        return discreteRange

    def isColumnMarkedForRow(self,row, columnLabel):
        if not columnLabel in row.index:
            return False
        elif row[columnLabel] == 0:
                return False
        
        return True

    
    def isAnyOperationAllowed(self):
        return self.isThisOperationAllowed(constants.OPERATION_ALLOWED_COLUMN_VALUE)

    def isSumOperationAllowed(self):
      
        isOperationAllowed = self.isAnyOperationAllowed()
        if not isOperationAllowed:
            return False
        return self.isThisOperationAllowed(constants.SUM_ALLOWED_COLUMN_VALUE)

    def isRangeOperationAllowed(self):
        isOperationAllowed = self.isAnyOperationAllowed()
        if not isOperationAllowed:
            return False
        return self.isThisOperationAllowed(constants.RANGE_ALLOWED_COLUMN_VALUE)

    def isPercentageOperationAllowed(self):
        isOperationAllowed = self.isAnyOperationAllowed()
        if not isOperationAllowed:
            return False

        return self.isThisOperationAllowed(constants.PERCENTAGE_ALLOWED_COLUMN_VALUE)

    def findDenominatorQuestion(self) -> str:
        searchResults : List[SearchResult] = self.findValueForMetadata(constants.DENOMINATOR_QUESTION_COLUMN_VALUE)
        if len(searchResults) == 0:
            return ""
        answer = searchResults[0].answer
        if answer == "" or answer =="nan":
            return ""
        else:
            return answer

    def searchInSelfForPercentage(self) -> bool:
        answers = self.findValueForMetadata(constants.PERCENTAGE_SEARCH_IN_SELF_COLUMN_VALUE)
        return self.checkResultHelper(answers)
    

    def findTemplate(self): 
        searchResults : List[SearchResult] = self.findValueForMetadata(constants.TEMPLATE_LABEL)
        if len(searchResults) == 0:
            return ""

        return searchResults[0].answer


    def checkResultHelper(self, searchResults : List[SearchResult]):
        if len(searchResults) == 0:
            return False
        elif str(searchResults[0].answer).lower() == constants.VALUE_FOR_ALLOW:
            return True

        return False

    def isThisOperationAllowed(self, operationLabel):
        answer = self.findValueForMetadata(operationLabel)
        return self.checkResultHelper(answer)


    def findValueForMetadata(self, metadataLabel):
        booleanSearchStrategy = DefaultShouldAddRowStrategy()
        operationAllowedEntity = createEntityObj(metadataLabel, entityLabel="none",  entityRole=None)
        searchResults = self.searchOnSparseMatrix([operationAllowedEntity], booleanSearchStrategy, False)
        return searchResults

    

    def searchOnSparseMatrix(self, entities, shouldAddRowStrategy, isSumAllowed):
        searchResults = []
        currentResultPointer = None
        entitiesUsed= []
        # get the underlying pandas dataframe from the internal data model
        sparseMatrixToSearchDf = self.getSparseMatrixDf()
        for i in range(sparseMatrixToSearchDf.shape[0]):
            row = sparseMatrixToSearchDf.loc[i]
            
            if "total" in row.index and sparseMatrixToSearchDf.loc[i,"total"] == 1:
                continue

            # entityValues = [e["value"] for e in entities]
            usedEntities = shouldAddRowStrategy.determineShouldAddRow(row, entities, self)

            shouldUseRow = len(usedEntities)>0
            # print(usedEntities)
            if shouldUseRow:
                if len(entitiesUsed) <= 0:
                    entitiesUsed = usedEntities

                newAnswer= sparseMatrixToSearchDf.loc[i,'Value']
                castedValue, type = self.determineResultType(newAnswer)
                # Get question for now. May need to check for out of range
                # print(len(self.questions))
                # print(self.questions)
                question = self.questions[i]
                newSearchResult : SearchResult = SearchResult(newAnswer, usedEntities, type, realQuestion= question )
                if currentResultPointer == None: 
                    # searchResult : SearchResult = SearchResult(newAnswer, usedEntities, type, self.questions[i])
                    currentResultPointer = newSearchResult
                    # currentResultPointer = str(currentResultPointer)
                    searchResults.append(currentResultPointer)
                else:
                    print("ADDING", newSearchResult.answer)
                   
                    currentResultPointer = self.addSearchResult(currentResultPointer, newSearchResult, searchResults, isSumAllowed)

                
        return searchResults


    #This function will determine the type of value the search result is: integer, float, string, percentage(string with % sign) 
    # and return the casted value along with enum value associated with that 
    def determineResultType(self,searchResult) -> Tuple[any, SearchResultType]:
        return self.typeController.determineResultType(searchResult)


    def addSearchResult(self, currentSearchResult : SearchResult, newSearchResult : SearchResult, searchResults : List[SearchResult], isSumAllowed) -> str:
        castedCurrValue, currentSearchResultType = self.determineResultType(currentSearchResult.answer)
        castedNewValue, newSearchResultType = self.determineResultType(newSearchResult.answer)

        if currentSearchResultType == SearchResultType.STRING:
            searchResults.append(newSearchResult)
            return newSearchResult

        if (currentSearchResultType == SearchResultType.FLOAT or currentSearchResultType == SearchResultType.NUMBER):
            if isSumAllowed and (newSearchResultType == SearchResultType.FLOAT or newSearchResultType == SearchResultType.NUMBER):
                newCalculatedValue = str(castedCurrValue + castedNewValue)
                currentSearchResult.changeAnswer(newCalculatedValue)
                if len(searchResults) == 0:
                    searchResults.append(currentSearchResult)
                # searchResults[len(searchResults)-1] = newCalculatedValue
                return currentSearchResult
            else:
                searchResults.append(newSearchResult)
                return newSearchResult

        elif currentSearchResultType == newSearchResultType and isSumAllowed:
            newCalculatedValue = str(castedCurrValue + castedNewValue)
            currentSearchResult.changeAnswer(newCalculatedValue)
            if len(searchResults) == 0:
                searchResults.append(currentSearchResult)

            return currentSearchResult
        else:
            searchResults.append(newSearchResult)
            return newSearchResult


    #This function will try to add up the search results, if the current search result and the new search result's type does not make sense
    # to be added together, it will add it into the list of answers instead of adding up the value.
    # def addSearchResult(self, currentSearchResult, newSearchResult, searchResults, isSumAllowed) -> str:
    #     castedCurrValue, currentSearchResultType = self.determineResultType(currentSearchResult)
    #     castedNewValue, newSearchResultType = self.determineResultType(newSearchResult)

    #     if (currentSearchResultType == SearchResultType.FLOAT or currentSearchResultType == SearchResultType.NUMBER):
    #         if isSumAllowed and (newSearchResultType == SearchResultType.FLOAT or newSearchResultType == SearchResultType.NUMBER):
    #             newCalculatedValue = str(castedCurrValue + castedNewValue)
    #             searchResults[len(searchResults)-1] = newCalculatedValue
    #             return newCalculatedValue
    #         else:
    #             searchResults.append(newSearchResult)
    #             return newSearchResult
    #     elif currentSearchResultType == SearchResultType.STRING:
    #         searchResults.append(newSearchResult)

    #     elif currentSearchResultType == newSearchResult:
    #         #Might move this common logic to a seperate function
    #         newCalculatedValue = str(castedCurrValue + castedNewValue)
    #         if len(searchResults) == 0:
    #             searchResults.append(newCalculatedValue)
    #         else:
    #             searchResults[len(searchResults)-1] = newCalculatedValue

    #         return newCalculatedValue
    #     else:
    #         searchResults.append(newSearchResult)

    #     return newSearchResult



