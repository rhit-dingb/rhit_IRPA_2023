from OutputController.Expression import Expression


class EntityExpression(Expression):
    def __init__(self, value):
        super().__init__(value, [])

    
    def evaluate(self,entities, answer):
        valueToReturn = ""
        indexToRemove = None
        for i in range(len(entities)):
            entity = entities[i]
            if entity["entity"] == self.value:
                valueToReturn =  entity["value"]
                indexToRemove = i
                break
        if indexToRemove:
            entities.pop(i)
        
        
        return valueToReturn


        