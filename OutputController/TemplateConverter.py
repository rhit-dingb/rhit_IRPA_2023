from typing import Dict, List
from OutputController.EntityExpression import EntityExpression
from OutputController.LiteralExpression import LiteralExpression
from OutputController.PhraseExpression import PhraseExpression
from OutputController.ValueExpression import ValueExpression
from OutputController.XorExpression import XorExpression
from Knowledgebase.DataModels.SearchResult import SearchResult
from OutputController.Expression import Expression


class TemplateConverter():
    """
    Class to construct full sentence response for data in which operation is performed on.
    The full sentence response is created using the template metadata in a particular sheet on the input excel file
    and the entities detected from the user query and on the actual question corresponding to the 
    answer being returned.

    The template converter works by parsing the template into different expression that can be evaluated 
    to diffferent values based its inner expression or the entities from the user query and on the actual question corresponding to the 
    answer being returned.
    """
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

    def parseTemplate(self,template : str) -> List[Expression]:
        """
        For the possible expressions on the template, please checkout the architecture and design document.
        Given a template string This function will recursively parse template string to create a 
        list of tree structure.
        Each space seperated token in a string is a expression which can have many child expressions 
        and each child expression and can have many child expression. "Evaluate" can be called on the 
        root expression to evaluate the entire expression tree recursively to return a final value.

        :param template: The template to parse into a list of expressions. 
        :return: List of expressions parsed from template.
        """
        if template == "" or template==" ":
            return []

        expressions = []
        currIndex = 0 
       
        while currIndex < len(template):
            # print(template[currIndex])
            if template[currIndex] in self.possibleBracket:
               
                matchIndex = self.lookForMatch(template[currIndex], currIndex+1 ,template)
                if matchIndex == -1:
                    raise Exception("No matching bracket found for "+ template[currIndex])
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
            


    def evaluateExpressions(self, expressions : List[Expression] , entities : List[Dict[str, str]], realQuestionEntities : List[Dict[str, str]], answer : str) -> List[str] : 
        """
        Given the list of expressions, an particular answer for a user questions, 
        entities detected from user query and the entities detected from the actual question corresponding to the answer
        return a list of string where each string is the result from evaluating each corresponding expression.
        """
        evaluatedValues = []  
        for expression in expressions:
           value = expression.evaluate(entities, realQuestionEntities, answer)
           evaluatedValues.append(value)
        return evaluatedValues

    
    def match(self,openBracket, closingBracket):
        """
        Given the opening bracket and closting bracket, determine if they match,
        representing a defined expression.
        """
        if openBracket == self.entityExpBracket and closingBracket == "]":
            return True

        if openBracket == self.phraseBracket and closingBracket == "}":
            return True

        if openBracket == self.valueBracket and closingBracket == ">":
            return True

        if openBracket == self.operationBracket and closingBracket == ")":
            return True



    def lookForMatch(self,bracket : str, start : int , template : str) -> int:
        """
        Given a start index in the template and the opening bracket, find the closing bracket that 
        match the opening brack and return the index of the closing bracket.
        """
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


    def constructOutput(self, searchResults : List[SearchResult], template) -> List[str]:
        fullSentenceAnswers = []
        expressions = self.parseTemplate(template)
        
        for searchResult in searchResults:
        #    print("CONSTRUCTING TEMPLATE FOR")
        #    print(searchResult.answer)
        #    print(searchResult.entitiesForRealQuestion)
           #Because EntityExpression remove an entity from the list when it uses that entity's value, I make a copy to keep the original in case we use it.
           entitiesCopy = searchResult.entitiesUsed.copy()
           realAnswerEntitiesCopy = searchResult.entitiesForRealQuestion.copy()
           answer = searchResult.answer
           sentenceTokens =  self.evaluateExpressions(expressions, entitiesCopy,realAnswerEntitiesCopy, answer)
           #Filter out empty string
           sentenceTokens = list(filter(lambda x: not x=="", sentenceTokens))
           sentence = " ".join(sentenceTokens)
           fullSentenceAnswers.append(sentence)

        # print(fullSentenceAnswers)
        return fullSentenceAnswers
            
        