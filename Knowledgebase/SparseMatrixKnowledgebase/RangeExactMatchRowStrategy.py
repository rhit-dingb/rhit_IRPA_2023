
from Knowledgebase.SparseMatrixKnowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy
from actions.entititesHelper import removeDuplicatedEntities
from Knowledgebase.SparseMatrixKnowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy


class RangeExactMatchRowStrategy(ShouldAddRowStrategy):
    """
    Strategy where a row must have exact column to entity match. If a row has other columns marked as one beside the given entities, the row will not be used
    likewise, if the list of entities has other entities besides the columns that are marked as 1 for the row, the row will not be used.(in the search)
    """
    def __init__(self):  
        super().__init__()
        self.defaultShouldAddRow = DefaultShouldAddRowStrategy()

    def determineShouldAddRow(self, row, entities, sparseMatrix):
        entities = removeDuplicatedEntities(entities)
        rangeFound  = sparseMatrix.findRangeForRow(row)
        rangeFound = list(filter(lambda x : not (x == None or x == float('-inf') or x == float('inf')), rangeFound ))
        rangeEntityValueProvided = []
        # matchCount = 0
        for entity in entities:
            try:
                entityValue = entity["value"]
                entityValue = float(entityValue)
                # if entityValue in row.index and row[entityValue] == 1 and entityValue in rangeFound:
                #     matchCount = matchCount + 1
                rangeEntityValueProvided.append(entityValue)
            except Exception:
                continue

        entitiesUsed = self.defaultShouldAddRow.determineShouldAddRow(row, entities, sparseMatrix)
        # print(row)
        # print(len(entitiesUsed))
        if len(entitiesUsed) > 0 and len(rangeFound) == len(rangeEntityValueProvided):
            return entities
        else:
            return []
        
                    
       