from copy import deepcopy
"""
Consist all the helpers for entities
"""

#There might be multiple of the same entity extracted, so might be better to use an array in the future?
def findEntityHelper(entities, key):
    for entityObj in entities:
        if entityObj["entity"] == key:
            return entityObj

    return None

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
    

def createEntityObj(entityValue, entityLabel="none",  entityRole=None):
        res = {"entity": entityLabel, "value": entityValue}
        if (entityRole):
            res["role"] = entityRole

        return res

