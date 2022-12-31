#Data model for aggregate discrete range result
from typing import Dict, List
from DataManager.constants import NUMBER_ENTITY_LABEL, RANGE_ENTITY_LABEL

from tests.testUtils import createEntityObjHelper


class RangeResultData():
    def __init__(self):
      # Each answer will correspond to a list of entities used
      self.answers = []
      self.entitiesUsedForAnswer : List[List[Dict[str, str]]] = []


    def addResult(self,answer, entitiesUsed):
        self.answers.append(answer)
        self.entitiesUsedForAnswer.append(entitiesUsed)


    def createFinalResultAndEntities(self,intention, isSumming, answers, entitiesUsedInEachSearch :  List[List[Dict[str, str]]] ):
        if isSumming:
            numbersUsed = []
            for entities in entitiesUsedInEachSearch:
                for entity in entities:
                    numbersUsed.append(entity["value"])
            
            finalEntities = self.constructRangeEntityHelper(intention, numbersUsed)
            self.addResult(answers[0], finalEntities)
        else:
            for answer, entities in zip(answers, entitiesUsedInEachSearch):
                self.addResult(answer,entities)

    def constructRangeEntityHelper(self, intention, numbersUsed):
        entities = []
        minEntity = createEntityObjHelper(min(numbersUsed), entityLabel=NUMBER_ENTITY_LABEL)
        maxEntity = createEntityObjHelper(max(numbersUsed), entityLabel=NUMBER_ENTITY_LABEL)
        if intention == "upperBound":
            rangeEntityWithWithinValue =  createEntityObjHelper("within", entityLabel=RANGE_ENTITY_LABEL)
        #If the intention is "between"
        elif intention == "between" or intention == "lowerBound":
            rangeEntityWithBetweenValue =  createEntityObjHelper("between", entityLabel=RANGE_ENTITY_LABEL)
            entities.append(rangeEntityWithBetweenValue)
            entities.append(minEntity)
            entities.append(maxEntity)

        return entities

