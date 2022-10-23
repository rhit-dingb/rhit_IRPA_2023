from copy import deepcopy

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