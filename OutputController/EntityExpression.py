from OutputController.Expression import Expression


class EntityExpression(Expression):
    def __init__(self, value):
        super().__init__(value, [])
        self.keyToCheck = "entity"
        self.entitiesOrigin = "user"

        self.useRealQuestionEntitiesSymbol = "^"
        self.useEntityValueSymbol = "*"

        self.REAL_QUESTION_ORIGIN = "realQuestion"

    
    def evaluate(self,entities, realQuestionEntities, answer):
        valueToReturn = ""
        indexToRemove = None
        if self.value == "":
            return ""
    
        entityValue = self.parseOp(self.value)
        entitiesToUse = entities
        if self.entitiesOrigin == self.REAL_QUESTION_ORIGIN:
            entitiesToUse = realQuestionEntities
        # else: 
        #     print("USE USER ENTITIES")
        #     print(entities)
            
        for i in range(len(entitiesToUse)):
            entity = entitiesToUse[i]
            if entity[self.keyToCheck] == entityValue:
                valueToReturn =  entity["value"]
                indexToRemove = i
                break

        if not indexToRemove == None:
            entitiesToUse.pop(i)
    
        return valueToReturn

    def parseOp(self, value):
        if value[0] == self.useEntityValueSymbol:
            self.keyToCheck = "value"
            return self.parseOp(value[1:])
        elif value[0] == self.useRealQuestionEntitiesSymbol:
            self.entitiesOrigin = self.REAL_QUESTION_ORIGIN
            return self.parseOp(value[1:])
        else: 
            return value


  

    


        