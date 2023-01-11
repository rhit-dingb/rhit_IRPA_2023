from OutputController.Expression import Expression


class PhraseExpression(Expression):
    def __init__(self, value, childExpression):
        super().__init__(value, childExpression)

    
    def evaluate(self,entities, answer):
        values = []
        anyExpressionFailToEvaluate = False
        entitiesCopy = entities.copy()
        for expression in self.childrenExpression:
            evaluatedValue = expression.evaluate(entitiesCopy, answer)
            if evaluatedValue == "":
                anyExpressionFailToEvaluate = True
            values.append(evaluatedValue)
        if anyExpressionFailToEvaluate:
            return ""
        else:
            entities[:] = entitiesCopy
            return " ".join(values)
            
    

        