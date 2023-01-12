from OutputController.Expression import Expression


class PhraseExpression(Expression):
    def __init__(self, value, childExpression):
        super().__init__(value, childExpression)

    
    def evaluate(self,entities,realAnswerEntities, answer):
        values = []
        anyExpressionFailToEvaluate = False
        entitiesCopy = entities.copy()  
        realAnswerEntitiesCopy = realAnswerEntities.copy()
        for expression in self.childrenExpression:
            evaluatedValue = expression.evaluate(entitiesCopy,realAnswerEntitiesCopy, answer)
            if evaluatedValue == "":
                anyExpressionFailToEvaluate = True
            values.append(evaluatedValue)
        if anyExpressionFailToEvaluate:
            return ""
        else:
            entities[:] = entitiesCopy
            realAnswerEntities[:] = realAnswerEntitiesCopy
            return " ".join(values)
            
    

        