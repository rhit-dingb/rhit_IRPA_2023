#List of ouput functions to control the ouptut of search in knowledgebase
# We might want to move the into classes later.


from Knowledgebase.constants import PERCENTAGE_FORMAT
from actions.entititesHelper import copyEntities
def constructSentence(answer, intent, printEntities): 
    return answer + "\n" + intent + "\n" + str(printEntities)   

#For high_school_units
def outputFuncForHighSchoolUnits(answer, intent, printEntities):
    response = "No units specified"
    if answer == 0:
        return constructSentence(response, intent, printEntities)
    else:
        print(type(answer))
        return  outputFuncForInteger(answer, intent, printEntities)

#For integer values
def outputFuncForInteger(answer, intent, printEntities):
    return constructSentence(str(int(answer)), intent,  printEntities)
    
#For percentage values
def outputFuncForPercentage(answer, intent, printEntities): 
    return constructSentence(PERCENTAGE_FORMAT.format(value = answer), intent, printEntities)

def outputFuncForText(answer, intent, printEntities):
    if answer == "":
        answer = "Sorry, I found no answer related to your question"
    return constructSentence(answer, intent, printEntities)
 
        

def identityFunc(answer, intent, printEntities):
    return (answer, intent, printEntities)

