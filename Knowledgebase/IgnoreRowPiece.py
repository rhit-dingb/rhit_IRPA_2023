"""
class to ignore a row if it has certain columns like "any-aid" or total(although is by default ignored in the search algorithm for now)
"""
from Knowledgebase.ShouldAddRowDecorator import ShouldAddRowDecorator
from Knowledgebase.ShouldAddRowInterface import ShouldAddRowInterface


class IgnoreRowPiece(ShouldAddRowDecorator):
    def __init__(self, decorated: ShouldAddRowInterface, targetedColumns):
        super().__init__(decorated)
        self.targetedColumns = targetedColumns

    def determineShouldAddRow(self, row, entities, sparseMatrix):
        for column in self.targetedColumns:
            if column in row and row[column] == 1:
                return (False, [])

        return self.decorated.determineShouldAddRow(row, entities, sparseMatrix)
