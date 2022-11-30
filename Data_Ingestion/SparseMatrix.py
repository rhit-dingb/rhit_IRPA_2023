"""
Internal data model representing a sparse matrix
"""

from typing import List
import pandas as pd


class SparseMatrix():
    def __init__(self, subSectionName, sparseMatrixDf):
        self.subSectionName = subSectionName
        self.sparseMatrixDf = sparseMatrixDf

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
