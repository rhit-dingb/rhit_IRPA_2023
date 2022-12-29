
# """
# Strategy where a row must have exact column to entity match. If a row has other columns marked as one beside the given entities, the row will not be used
# likewise, if the list of entities has other entities besides the columns that are marked as 1 for the row, the row will not be used.(in the search)
# """
from DataManager.constants import NUMBER_ENTITY_LABEL
from Knowledgebase.ShouldAddRowInterface import ShouldAddRowInterface
from actions.entititesHelper import findMultipleSameEntitiesHelper, removeDuplicatedEntities




class RangeExactMatchRowStrategy(ShouldAddRowInterface):
    def __init__(self):
        super().__init__()

        
    def determineShouldAddRow(self, row, entities, sparseMatrix):
        entities = removeDuplicatedEntities(entities)
        rangeFound  = sparseMatrix.findRangeForRow(row)
        rangeFound = list(filter(lambda x : not (x == None or x == float('-inf') or x == float('inf')), rangeFound ))
        rangeEntityValueProvided = []

        matchCount = 0
        for entity in entities:
            try:
                entityValue = entity["value"]
                entityValue = float(entityValue)
                # if entityValue in row.index and row[entityValue] == 1 and entityValue in rangeFound:
                #     matchCount = matchCount + 1
                rangeEntityValueProvided.append(entityValue)
            except Exception:
                continue

        for valueFound in rangeFound:
            for rangeProvided in rangeEntityValueProvided:
                if valueFound == rangeProvided:
                    matchCount = matchCount + 1
                    continue

        if matchCount == len(rangeEntityValueProvided) and len(rangeFound) == len(rangeEntityValueProvided):

            return entities
        else:
            return []
        
                    
       