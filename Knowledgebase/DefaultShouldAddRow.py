from Knowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy
"""
Default strategy to determine whether a row should be added. More detail below
"""
class DefaultShouldAddRowStrategy(ShouldAddRowStrategy):
    """
    Given a row in the sparse matrix and a list of entities, this function implementation 
    will check each entity to see if the column value for that entity is 1. If all the entity's corresponding
    column value is 1, it will return true, otherwise false.
    row: current row of sparse matrix in question
    entities: list of entity 
    """
    def determineShouldAddRow(self, row, entities):
        temp_count = 0
        for entity in row.index:
            if entity in entities: 
                if row[entity] == 1:
                    temp_count += 1
        if temp_count == len(entities):
            return True
        else: 
            return False 
        
                

