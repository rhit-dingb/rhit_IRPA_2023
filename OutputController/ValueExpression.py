from OutputController.Expression import Expression


class ValueExpression(Expression):
    def __init__(self, value):
        super().__init__(value, [])

    
    def evaluate(self,entities,realAnswerEntities, answer):
        return answer
            
    

        