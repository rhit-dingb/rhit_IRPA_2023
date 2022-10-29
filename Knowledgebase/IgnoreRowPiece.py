"""
class to ignore a row if it has certain columns like "any-aid" or total(although is by default ignored in the search algorithm for now)
"""
from Knowledgebase.ShouldAddRowDecorator import ShouldAddRowDecorator
from Knowledgebase.ShouldAddRowInterface import ShouldAddRowInterface


class IgnoreRowPiece(ShouldAddRowDecorator):
    def __init__(self, decorated : ShouldAddRowInterface, targetedColumns):
         super().__init__(decorated)
         self.targetedColumns = targetedColumns
        

    def determineShouldAddRow(self, row, entities):
        for column in self.targetedColumns:
            if row[column] == 1:
                return []

        return self.decorated.determineShouldAddRow(row, entities)
