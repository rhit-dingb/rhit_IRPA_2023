from Knowledgebase.ShouldAddRowInterface import ShouldAddRowInterface


class ShouldAddRowStrategy(ShouldAddRowInterface):
    def __init__(self):
        super().__init__()
        
    def determineShouldAddRow(self, row, entities):
        raise Exception("This method should be implemented by a concrete class")
