from copy import deepcopy
"""
Consist all the helpers to process entity obj extracted by rasa.
"""


def findCharIndexForWord(word, question):
    for i in range(len(question)):
        found = True
        currIndex = i
        for j in range(len(word)):
            if currIndex >= len(question): 
                return (None, None)
            if question[currIndex] == word[j]:
                currIndex = currIndex +1
            else:
                found = False
                break
        if found:
            return (i, currIndex-1)
    return (None, None)


def findEntityHelper(entities, key, by="entity"):
    entitiesFound = findMultipleSameEntitiesHelper(entities, key, by)
    if len(entitiesFound) == 0:
        return None
    return entitiesFound[0]


def findMultipleSameEntitiesHelper(entities, key, by= "entity"):
    res = []
    for entityObj in entities:
        if entityObj[by] == key:
            res.append(entityObj)
    return res

def copyEntities(entities):
    entitiesExtractedCopy = deepcopy(entities)
    return entitiesExtractedCopy

def filterEntities(entities, toFilter):
    res = []
    for entityObj in entities:
        if not entityObj["entity"] in toFilter:
            res.append(entityObj)
    return res

def removeDuplicatedEntities(entities):
    uniqueEntityValuesFound = []
    uniqueEntities = []
    for entity in entities:
        entityValue = entity["value"]
        if not entityValue in uniqueEntityValuesFound:
            uniqueEntityValuesFound.append(entityValue)
            uniqueEntities.append(entity)
    return uniqueEntities
    


def changeEntityValue(entities, targetLabel, newValue):
    for entity in entities: 
        if targetLabel in entity["entity"]:
            entity["value"] = newValue

def changeEntityValueByRole(entities, targetEntity, targetRole, newValue):
    for entity in entities: 
        if targetEntity in entity["entity"] and hasattr(entity, "role") and targetRole in entity["role"]:
            entity["value"] = newValue
    

def createEntityObj(entityValue, entityLabel="none",  entityRole=None):
        res = {"entity": entityLabel, "value": entityValue}
        if (entityRole):
            res["role"] = entityRole

        return res

