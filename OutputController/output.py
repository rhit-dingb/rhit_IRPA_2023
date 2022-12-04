#List of ouput functions to control the ouptut of search in knowledgebase
# We might want to move the into classes later.

from Knowledgebase.constants import PERCENTAGE_FORMAT
from actions.entititesHelper import copyEntities
NO_ANSWER_FOUND_RESPONSE = "Sorry, I found no answer related to your question"

def constructSentence(answers, intent, entitiesUsed, noAnswerResponse = NO_ANSWER_FOUND_RESPONSE): 
    if len(answers) == 0 or answers[0] == "" or answers[0] == None:
       answer = noAnswerResponse
       return [answer]
    
    sentences = []
    for answer in answers:
        sentence = answer + "\n" + intent + "\n" + str(entitiesUsed) 
        sentences.append(sentence)

    return sentences

#For high_school_units
def outputFuncForHighSchoolUnits(answers, intent, entitiesUsed):
        return  outputFuncForInteger(answers, intent, entitiesUsed, "no units specified")

#For integer values
def outputFuncForInteger(answer : int, intent, entitiesUsed):
    return constructSentence(str(answer), intent,  entitiesUsed)
    
#For percentage values
def outputFuncForPercentage(answer : float, intent, entitiesUsed): 
    return constructSentence(PERCENTAGE_FORMAT.format(value = answer), intent, entitiesUsed)

def outputFuncForText(answer : str, intent, entitiesUsed):
    return constructSentence(answer, intent, entitiesUsed)
 

def identityFunc(answers, intent, entitiesUsed):
    return (answers, intent, entitiesUsed)

