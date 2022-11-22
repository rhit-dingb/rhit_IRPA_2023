from Knowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy
"""
Default strategy to determine whether a row of a sparse matrix should be used in the total value while searching. More detail below
"""


class DefaultShouldAddRowStrategy(ShouldAddRowStrategy):
    def __init__(self):
        super().__init__()
        
    """
    Given a row in the sparse matrix and a list of entities, this function implementation 
    will check each entity to see if the column value for that entity is 1. If all the entity's corresponding
    column value is 1, it will return true, otherwise false.
    row: current row of sparse matrix in question -- a row in the pandas dataframe
    entities: list of entity 
    """

    def determineShouldAddRow(self, row, entities):
        temp_count = 0

        # Note: we only want to consider entities that are supported by this sparse matrix, so we can answer the user's question as best as possible
        filteredEntities = []
        #processedColumn = [column.replace(" ", "") for column in row.index]
        processedColumn = row.index
        print(entities)
        print(processedColumn)
      
        
        for entity in entities:
            if entity in processedColumn:
                filteredEntities.append(entity)

     
        # filteredEntities = set(filteredEntities)
        for column in processedColumn:
            if column in filteredEntities:
               
                if row[column] == 1:
                    temp_count = temp_count + 1

        if temp_count == len(filteredEntities):
            return filteredEntities
        else:
            return []
