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
        # for entity in entities:
        #     if entity in self.sparseMatrixDf.columns:
        #         entitiesMatchCount = entitiesMatchCount+1

        # return entitiesMatchCount

    
    # #This function determines how many elements in the first array is in the second array.
    def determineMatchCountHelper(self, entities: List[str], columns: List[str]):
        entitiesMatchCount = 0
        for entity in entities:
            if entity in columns:
                entitiesMatchCount = entitiesMatchCount + 1

        return entitiesMatchCount


    def findMaxBoundLowerBoundForDiscreteRange(self):
        ranges = self.findAllDiscreteRange()
        print(ranges)
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

    
    def isOperationSupported(self):
        booleanSearchStrategy = DefaultShouldAddRowStrategy()
        operationAllowedEntity = createEntityObj(constants.OPERATION_ALLOWED_COLUMN_VALUE, entityLabel="none",  entityRole=None)
        searchResult, entitiesUsed = self.searchOnSparseMatrix([operationAllowedEntity], booleanSearchStrategy)
        if len(searchResult) == 0:
            return False
        elif searchResult[0] == constants.VALUE_FOR_ALLOW:
            return True
            
        return False

    def searchOnSparseMatrix(self,entities, shouldAddRowStrategy):
        searchResults = []
        searchResult = None
        entitiesUsed= []
        # get the underlying pandas dataframe from the internal data model
        sparseMatrixToSearchDf = self.getSparseMatrixDf()
        for i in range(sparseMatrixToSearchDf.shape[0]):
            row = sparseMatrixToSearchDf.loc[i]
            
            if "total" in row.index and sparseMatrixToSearchDf.loc[i,"total"] == 1:
                continue
           
            usedEntities = shouldAddRowStrategy.determineShouldAddRow(row, entities, self)
            shouldUseRow = len(usedEntities)>0
            # print(usedEntities)
           
            if shouldUseRow:
                newSearchResult = sparseMatrixToSearchDf.loc[i,'Value']
                if searchResult == None: 
                    searchResult, type = self.determineResultType(newSearchResult)
                    searchResult = str(searchResult)
                    searchResults.append(searchResult)
                else:
                    searchResult = self.addSearchResult(searchResult, newSearchResult, searchResults)

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


    # def determineBestMatchRow(self, entities):
    #     maxMatchCount = None
    #     minNonMatchCount = None
    #     bestMatchedRows = []
    #     finalBestMatch = None

    #     for i in range(self.sparseMatrixDf.shape[0]):
    #         row = self.sparseMatrixDf.loc[i]
    #         matchCount, numberOfColumnsNotMatchedByEntity = self.determineEntityMatchToRowCounts(entities, row)

    #         if maxMatchCount is None or (matchCount >= maxMatchCount):

    #             maxMatchCount = matchCount
    #             if (matchCount == maxMatchCount):
    #                 bestMatchedRows.append(row)
    #             else if (matchCount>maxMatchCount):
    #                 maxMatchCount = matchCount
    #                 bestMatchedRows = []

    #     return (maxMatchCount, bestMatchedRow)

    # def determineEntityMatchToRowCounts(self, entities, row): 
    #     columnLabelsMarkedAsOneForGivenRow = []
    #     for columnLabel in row.index:
    #         if row[columnLabel] == 1:
    #             columnLabelsMarkedAsOneForGivenRow.append(columnLabel)

    #     matchCountForEntityAgainstRow = self.determineMatchCountHelper(entities, columnLabel),
    #     numberOfColumnsNOTMatchedByEntityExtracted = len(columnLabelsMarkedAsOneForGivenRow) - len(entities)
    #     return (matchCountForEntityAgainstRow, numberOfColumnsNOTMatchedByEntityExtracted)


# def findRowsOverlapWithGivenRow(self, givenRow):
#         if not "overlap" in givenRow.index:
#             return []
#         else:
#             overlapRows = []
#             columnMarkedAsOneForGivenRow = []
#             for column in givenRow.index:
#                 if row[column] == 1:
#                     columnMarkedAsOneForGivenRow.append(column)

#             for i in range(self.sparseMatrixDf.shape[0]):
#                 row = self.sparseMatrixDf.loc[i]

#                 for column in row.index:
#                     doesOverlap = True
#                     if row[column] == 1:
#                         if not column in columnMarkedAsOneForGivenRow:
#                             doesOverlap = False
#                             break

#                     if doesOverlap:
#                         overlapRows.append(row)

#             return overlapRows
