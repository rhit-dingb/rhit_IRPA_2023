from OutputController.Expression import Expression


class XorExpression(Expression):
    def __init__(self, value, expressions):
        super().__init__(value, expressions)

    
    def evaluate(self,entities, answer):
        print(len(self.childrenExpression))
        for expression in self.childrenExpression:
            value = expression.evaluate(entities, answer)
            if not value == "":
                return value
        
        return ""
            
    

        