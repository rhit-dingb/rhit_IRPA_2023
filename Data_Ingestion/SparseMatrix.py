"""
Internal data model representing a sparse matrix
"""

from typing import List, Tuple
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.SearchResultType import SearchResultType

from Knowledgebase.TypeController import TypeController
from actions.entititesHelper import createEntityObj
import Data_Ingestion.constants as constants



class SparseMatrix():
    def __init__(self, subSectionName, sparseMatrixDf):
        self.subSectionName = subSectionName
        self.sparseMatrixDf = sparseMatrixDf
        self.typeController = TypeController()
       

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
            discreteRange.insert(0,  None)

        return discreteRange

    
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

    def checkResultHelper(self, searchResults):
        if len(searchResults) == 0:
            return False
        elif str(searchResults[0]).lower() == constants.VALUE_FOR_ALLOW:
            return True

        return False

    def isThisOperationAllowed(self, operationName):
        booleanSearchStrategy = DefaultShouldAddRowStrategy()
        operationAllowedEntity = createEntityObj(operationName, entityLabel="none",  entityRole=None)
        searchResult, entitiesUsed = self.searchOnSparseMatrix([operationAllowedEntity], booleanSearchStrategy, False)
        return self.checkResultHelper(searchResult)

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

            entityValues = [e["value"] for e in entities]
            usedEntities = shouldAddRowStrategy.determineShouldAddRow(row, entityValues, self)
            shouldUseRow = len(usedEntities)>0
            # print(usedEntities)
           
            if shouldUseRow:
                newSearchResult = sparseMatrixToSearchDf.loc[i,'Value']
                if currentResultPointer == None: 
                    currentResultPointer, type = self.determineResultType(newSearchResult)
                    currentResultPointer = str(currentResultPointer)
                    searchResults.append(currentResultPointer)
                else:
                    currentResultPointer = self.addSearchResult(currentResultPointer, newSearchResult, searchResults, isSumAllowed)

                if len(entitiesUsed) <= 0:
                    entitiesUsed = usedEntities
        entitiesUsed = list(entitiesUsed)
        return (searchResults, entitiesUsed)


    #This function will determine the type of value the search result is: integer, float, string, percentage(string with % sign) 
    # and return the casted value along with enum value associated with that 
    def determineResultType(self,searchResult) -> Tuple[any, SearchResultType]:
        return self.typeController.determineResultType(searchResult)

    #This function will try to add up the search results, if the current search result and the new search result's type does not make sense
    # to be added together, it will add it into the list of answers instead of adding up the value.
    def addSearchResult(self, currentSearchResult, newSearchResult, searchResults, isSumAllowed) -> str:
        castedCurrValue, currentSearchResultType = self.determineResultType(currentSearchResult)
        castedNewValue, newSearchResultType = self.determineResultType(newSearchResult)
        if (currentSearchResultType == SearchResultType.FLOAT or currentSearchResultType == SearchResultType.NUMBER):
            if isSumAllowed and (newSearchResultType == SearchResultType.FLOAT or newSearchResultType == SearchResultType.NUMBER):
                newCalculatedValue = str(castedCurrValue + castedNewValue)
                searchResults[len(searchResults)-1] = newCalculatedValue
                return newCalculatedValue
            else:
                searchResults.append(newSearchResult)
                return newSearchResult

        else:
            searchResults.append(newSearchResult)

        return newSearchResult

