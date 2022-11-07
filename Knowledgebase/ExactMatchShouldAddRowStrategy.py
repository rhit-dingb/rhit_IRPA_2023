from Knowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy
"""
Strategy where a row must have exact column to entity match. If a row has other columns marked as one beside the given entities, the row will not be used
likewise, if the list of entities has other entities besides the columns that are marked as 1 for the row, the row will not be used.(in the search)
"""
class ExactMatchShouldAddRowStrategy(ShouldAddRowStrategy):
    def __init__(self):
        super().__init__()
        
    def determineShouldAddRow(self, row, entities):
        for entity in entities:
            if entity in row.index and row[entity]  == 0:
                return [] 
        
        for column in row.index: 
            if row[column] == 1:
                if not column in entities:
                    return []
              
        return entities    