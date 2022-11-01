#List of ouput functions to control the ouptut of search in knowledgebase
# We might want to move the into classes later.


from Knowledgebase.constants import PERCENTAGE_FORMAT
from actions.entititesHelper import copyEntities
def constructSentence(answer, intent, printEntities): 
    return answer + "\n" + intent + "\n" + str(printEntities)   

#For integer values
def outputFuncForInteger(answer, intent, printEntities):
    return constructSentence(str(int(answer)), intent,  printEntities)
    
#For percentage values
def outputFuncForPercentage(answer, intent, printEntities): 
    return constructSentence(PERCENTAGE_FORMAT.format(value = answer), intent, printEntities)

def identityFunc(answer, intent, printEntities):
    return (answer, intent, printEntities)