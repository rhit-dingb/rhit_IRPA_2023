from Knowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy

class DefaultShouldAddRowStrategy(ShouldAddRowStrategy):
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
        
                

