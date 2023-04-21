#Data model for aggregate discrete range result
from typing import Dict, List
from DataManager.constants import NUMBER_ENTITY_LABEL, RANGE_ENTITY_LABEL
from actions.entititesHelper import getEntityValueHelper
from Knowledgebase.DataModels.SearchResult import SearchResult

from actions.entititesHelper import createEntityObj


class RangeResultData():
    def __init__(self):
      # Each answer will correspond to a list of entities used
      self.answers = []
      self.entitiesUsedForAnswer : List[List[Dict[str, str]]] = []


    def addResult(self,answer : SearchResult, entitiesUsed):
        self.answers.append(answer)
        answer.entitiesUsed = entitiesUsed
        self.entitiesUsedForAnswer.append(entitiesUsed)


    def createFinalResultAndEntities(self,rangeToCreateEntityFor, searchResults : List[SearchResult] ):
        intention = None
        # print("RANGE TO CREATE ENTTIY FOR")
        # print(rangeToCreateEntityFor)
        for range, searchResult in zip(rangeToCreateEntityFor, searchResults):
            if range[0] == float('-inf'):
                intention = "upperBound"
            elif range[1] == float('inf'):
                intention = "lowerBound"
            else:
                intention = "between"
            
            # entityValues =  getEntityValueHelper(searchResult.entitiesUsed)
            # print("ENTITY VALUES")
            # print(entityValues)
            finalEntities = self.constructRangeEntityHelper(intention, range)
            self.addResult(searchResult, finalEntities)

        # if isSumming:
        #     numbersUsed = []
        #     for entities in entitiesUsedInEachSearch:
        #         entityValues =  getEntityValueHelper(entities)
        #         numbersUsed = numbersUsed + entityValues
        #     finalEntities = self.constructRangeEntityHelper(intention, numbersUsed)
        #     self.addResult(answers[0], finalEntities)
        # else:
        #     for answer, entities in zip(answers, entitiesUsedInEachSearch):
        #         intention = "between"
        #         if len(entities) == 1: 
        #             intention = "upperBound"
        #         entityValues =  getEntityValueHelper(entities)
        #         finalEntities = self.constructRangeEntityHelper(intention, entityValues)
        #         self.addResult(answer, finalEntities)

    def constructRangeEntityHelper(self, intention, numbersUsed):
        entities = []
        minEntity = createEntityObj(min(numbersUsed), entityLabel=NUMBER_ENTITY_LABEL)
        maxEntity = createEntityObj(max(numbersUsed), entityLabel=NUMBER_ENTITY_LABEL)

        # print(entities)
        if intention == "upperBound":
            rangeEntityUpperBound =  createEntityObj("within", entityLabel=RANGE_ENTITY_LABEL)
            entities.append(rangeEntityUpperBound)
            entities.append(maxEntity)
        elif intention == "lowerBound":
            rangeEntityLowerBound=  createEntityObj("more than", entityLabel=RANGE_ENTITY_LABEL)
            entities.append(rangeEntityLowerBound)
            entities.append(minEntity)
        #If the intention is "between"
        elif intention == "between":
            rangeEntityWithBetweenValue =  createEntityObj("between", entityLabel=RANGE_ENTITY_LABEL)
            entities.append(rangeEntityWithBetweenValue)
            entities.append(minEntity)
            entities.append(maxEntity)

        return entities

