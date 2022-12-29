from OutputController.Expression import Expression


class PhraseExpression(Expression):
    def __init__(self, value, childExpression):
        super().__init__(value, childExpression)

    
    def evaluate(self,entities, answer):
        values = []
        anyExpressionFailToEvaluate = False
        for expression in self.childrenExpression:
            evaluatedValue = expression.evaluate(entities, answer)
            if evaluatedValue == "":
                anyExpressionFailToEvaluate = True
            values.append(evaluatedValue)
        if anyExpressionFailToEvaluate:
            return ""
        else:
            return " ".join(values)
            
    

        