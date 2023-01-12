class Expression():
    def __init__(self, value, childrenExpression):
        self.value = value
        self.childrenExpression = childrenExpression

    
    def evaluate(entities, realAnswerEntities ,answer):
        raise Exception("please implement this with a concrete subclass")

        