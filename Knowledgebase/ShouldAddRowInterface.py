"""
"interface" for providing common abstraction for ShouldAddRowDecorator and the base ShouldAddRowStrategy
"""


class ShouldAddRowInterface():

    def determineShouldAddRow(self, row, entities, sparseMatrix):
        raise Exception("This method should be implemented by a concrete class")
