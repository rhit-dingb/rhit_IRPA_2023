"""
"Abstract" class for implementing decorator pattern for the determination of if a row should be added 
"""
from Knowledgebase.ShouldAddRowInterface import ShouldAddRowInterface


class ShouldAddRowDecorator(ShouldAddRowInterface):
    def __init__(self, decorated):
        self.decorated = decorated

    def determineShouldAddRow(self, row, entities):
        raise Exception("This method should be implemented by a concrete class")

