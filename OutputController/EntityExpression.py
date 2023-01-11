from OutputController.Expression import Expression


class EntityExpression(Expression):
    def __init__(self, value):
        super().__init__(value, [])

    
    def evaluate(self,entities, answer):
        valueToReturn = ""
        indexToRemove = None
        if self.value == "":
            return ""
        
        keyToCheck = "entity"
        if self.value[0] == "*":
            self.value = self.value[1:]
            keyToCheck = "value"

        for i in range(len(entities)):
            entity = entities[i]
            if entity[keyToCheck] == self.value:
                valueToReturn =  entity["value"]
                indexToRemove = i
                break

        if not indexToRemove == None:
            entities.pop(i)
    
        return valueToReturn


  

    


        