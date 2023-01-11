from typing import List
from OutputController.EntityExpression import EntityExpression
from OutputController.LiteralExpression import LiteralExpression
from OutputController.PhraseExpression import PhraseExpression
from OutputController.ValueExpression import ValueExpression
from OutputController.XorExpression import XorExpression
from Knowledgebase.DataModels.SearchResult import SearchResult


class TemplateConverter():
    def __init__(self):
        self.entityExpBracket = "["
        self.phraseBracket = "{"
        self.valueBracket = "<"
        self.operationBracket = "("
        self.possibleBracket = [
            self.entityExpBracket,
            self.phraseBracket,
            self.valueBracket,
            self.operationBracket
        ]

    def parseTemplate(self,template):
        if template == "" or template==" ":
            return []

        expressions = []
        currIndex = 0 
       
        while currIndex < len(template):

            if template[currIndex] in self.possibleBracket:
               
                matchIndex = self.lookForMatch(template[currIndex], currIndex+1 ,template)
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
                elif template[currIndex] == self.operationBracket:
                    tokens = newTemplate.split(" ")
                    if len(tokens) == 0:
                        raise Exception("No operation provided")
                    else:
                        tokensToParse = tokens[1:]
                        tokensToParse = " ".join(tokensToParse)
                        # print("TOKEN TO PARSE")
                        # print(tokensToParse)
                        opExpression = self.determineOperation(tokens[0])
                        expressionsParsed = self.parseTemplate(tokensToParse)

                        opExpression.childrenExpression = expressionsParsed
                        opExpression.value = newTemplate
                        expressions.append(opExpression)

                currIndex = matchIndex

            elif template[currIndex] == " ":
                currIndex = currIndex + 1
                continue
            else: 
                for i in range(currIndex, len(template)):
                    if i == len(template)-1 or template[i+1] == " " :
                        value = template[currIndex:i+1]
                        literalExpression = LiteralExpression(value)
                        expressions.append(literalExpression)
                        currIndex = i
                        break
            currIndex = currIndex + 1 
        return expressions

    def determineOperation(self, token):
        if token.lower() == "xor":
            return XorExpression("", [])
        else: 
            raise Exception("Operation not supported")
            


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

        if openBracket == self.operationBracket and closingBracket == ")":
            return True



    def lookForMatch(self,bracket, start, template):
        stack = []
        stack.append(bracket)
        for i in range(start, len(template)):
            if template[i] == bracket:
                stack.append(template[i])
            elif self.match(bracket, template[i]):
                stack.pop()
                if len(stack) == 0:
                    return i
                else:
                    continue
        return -1


    def constructOutput(self, searchResults : List[SearchResult], template):
        fullSentenceAnswers = []
        expressions = self.parseTemplate(template)
        
        for searchResult in searchResults:
           #Because EntityExpression remove an entity from the list when it uses that entity's value, I make a copy to keep the original in case we use it.
           entitiesCopy = searchResult.entitiesUsed.copy()
           answer = searchResult.answer
           sentenceTokens =  self.evaluateExpressions(expressions, entitiesCopy, answer)
           #Filter out empty string
           sentenceTokens = list(filter(lambda x: not x=="", sentenceTokens))
           sentence = " ".join(sentenceTokens)
           fullSentenceAnswers.append(sentence)
           
        print(fullSentenceAnswers)
        return fullSentenceAnswers
            
        