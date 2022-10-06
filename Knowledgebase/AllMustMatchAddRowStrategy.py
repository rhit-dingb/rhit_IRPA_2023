from Knowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy

class AllMustMatchAddRowStrategy(ShouldAddRowStrategy):
    def determineShouldAddRow(self, row, entities):
        temp_count = 0
        matrixColumns = row.index
        hasAllSpecifiedEntities = True
        hasNoOtherColumnMarkedAsOneOtherThanExtractedEntities = True
        for extractedEntity in entities:
            if not extractedEntity in matrixColumns: 
                hasAllSpecifiedEntities = False
                
        for column in row.index:
            if row[column] == 1 and not column in entities:
                hasNoOtherColumnMarkedAsOneOtherThanExtractedEntities = False
        
        return hasAllSpecifiedEntities and hasNoOtherColumnMarkedAsOneOtherThanExtractedEntities

        
                