from OutputController.Expression import Expression


class LiteralExpression(Expression):
    def __init__(self, value):
       super().__init__(value, [])

    
    def evaluate(self, entities, answer):
        return self.value
        

        