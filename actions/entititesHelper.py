from copy import deepcopy
"""
Consist all the helpers to process entity obj extracted by rasa.
"""


def findEntityHelper(entities, key):
    entitiesFound = findMultipleSameEntitiesHelper(entities, key)
    if len(entitiesFound) == 0:
        return None
    return entitiesFound[0]


def findMultipleSameEntitiesHelper(entities, key):
    res = []
    for entityObj in entities:
        if entityObj["entity"] == key:
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

