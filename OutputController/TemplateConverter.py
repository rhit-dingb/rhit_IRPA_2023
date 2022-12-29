from OutputController.EntityExpression import EntityExpression
from OutputController.LiteralExpression import LiteralExpression
from OutputController.PhraseExpression import PhraseExpression
from OutputController.ValueExpression import ValueExpression


class TemplateConverter():
    def __init__(self):
        self.entityExpBracket = "["
        self.phraseBracket = "{"
        self.valueBracket = "<"
        self.possibleBracket = [
            self.entityExpBracket,
            self.phraseBracket,
            self.valueBracket
        ]

    def parseTemplate(self,template):
        if template == "" or template==" ":
            return []

        expressions = []
        currIndex = 0 
       
        while currIndex < len(template):

            if template[currIndex] in self.possibleBracket:
               
                matchIndex = self.lookForMatch(template[currIndex], currIndex ,template)
                if matchIndex == -1:
                    raise Exception("No matching bracket found for"+self.entityExpBracket)
                # expressionsParsed = self.parseTemplate(newTemplate)
                newTemplate = template[currIndex+1:matchIndex]
                # print("STARTING AGAIN on"+str(currIndex))
                # print("FOUND MATCH On"+ str(matchIndex))
               
                if template[currIndex] == self.entityExpBracket:
                    entityExpression = EntityExpression(newTemplate)
                    expressions.append(entityExpression)
                elif template[currIndex] == self.phraseBracket:
                    expressionsParsed = self.parseTemplate(newTemplate)
                    phraseExpression = PhraseExpression(newTemplate, expressionsParsed)
                    expressions.append(phraseExpression)
                elif template[currIndex] == self.valueBracket:
                    valueExpression = ValueExpression(newTemplate)
                    expressions.append(valueExpression)

                currIndex = matchIndex

            elif template[currIndex] == " ":
                currIndex = currIndex + 1
                continue
            else: 
                for i in range(currIndex, len(template)):
                    if template[i] == " " or i == len(template)-1:
                        value = template[currIndex:i]
                        literalExpression = LiteralExpression(value)
                        expressions.append(literalExpression)
                        currIndex = i
                        break
                

            currIndex = currIndex + 1 

        return expressions

    def evaluateExpressions(self, expressions,entities,  answer): 
        evaluatedValues = []  
        for expression in expressions:
           value = expression.evaluate(entities, answer)
           evaluatedValues.append(value)
        return evaluatedValues

    
    def match(self,openBracket, closingBracket):
        if openBracket == self.entityExpBracket and closingBracket == "]":
            return True

        if openBracket == self.phraseBracket and closingBracket == "}":
            return True

        if openBracket == self.valueBracket and closingBracket == ">":
            return True



    def lookForMatch(self,bracket, start, template):
        for i in range(start, len(template)):
            if self.match(bracket, template[i]):
                return i

        return -1


    def constructOutput(self,answers, entitiesUsed, template):
        fullSentenceAnswers = []
        expressions = self.parseTemplate(template)
        for answer in answers:
           sentence =  self.evaluateExpressions(expressions, entitiesUsed, answer)
           sentence = " ".join(sentence)
           fullSentenceAnswers.append(sentence)

        return fullSentenceAnswers
            
        