#List of ouput functions to control the ouptut of search in knowledgebase
# We might want to move the into classes later.


from Knowledgebase.constants import PERCENTAGE_FORMAT
from actions.entititesHelper import copyEntities
NO_ANSWER_FOUND_RESPONSE = "Sorry, I found no answer related to your question"

def constructSentence(answer, intent, entitiesUsed): 
    if answer == "" or answer == None or answer.lower() == "none":
       answer = NO_ANSWER_FOUND_RESPONSE
    return answer + "\n" + intent + "\n" + str(entitiesUsed)   

#For high_school_units
def outputFuncForHighSchoolUnits(answer, intent, entitiesUsed):
    response = "no units specified"
    if answer == 0:
        return constructSentence(response, intent, entitiesUsed)
    else:
        print(type(answer))
        return  outputFuncForInteger(answer, intent, entitiesUsed)

#For integer values
def outputFuncForInteger(answer, intent, entitiesUsed):
    return constructSentence(str(int(answer)), intent,  entitiesUsed)
    
#For percentage values
def outputFuncForPercentage(answer, intent, entitiesUsed): 
    return constructSentence(PERCENTAGE_FORMAT.format(value = answer), intent, entitiesUsed)

def outputFuncForText(answer, intent, entitiesUsed):
    return constructSentence(answer, intent, entitiesUsed)
 
        

def identityFunc(answer, intent, entitiesUsed):
    return (answer, intent, entitiesUsed)

