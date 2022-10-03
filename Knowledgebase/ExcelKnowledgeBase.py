
from Knowledgebase.Knowledgebase import KnowledgeBase
from Knowledgebase.LevenshteinMatcher import LevenshteinMatcher
from Data_Ingestion.ExcelProcessor import ExcelProcessor
import pandas as pd
import copy

"""
"""

class ExcelKnowledgeBase(KnowledgeBase):
    def __init__(self, filePath):
        self.filePath = filePath
        self.excelProcessor = ExcelProcessor()
        self.topicToParse = ["general_enrollment"]
        self.data = self.excelProcessor.processExcel(filePath, self.topicToParse)
        #use this matcher for now, if it is not doing too good we can swap it out.
        self.matcher = LevenshteinMatcher(2)

    def initialize():
      pass


    def getAvailableOptions(self, intent, entities):
      def getKeys(res):
        return res.keys()

      return self.searchForAnswer(intent, entities, getKeys)

    def searchForAnswer(self, intent, entities, outputStrategy):
      #Algorithm to search in knowledgebase for answers:
      #For given intent, access the data.
      #Use matcher - first check if anything match, if so, drill down, remove that entity
      #In the new drill downed part, check for anything match, if so drill down.
      #  If not, apply the output function on the remaining data
      if intent.lower() not in self.data:
        raise Exception("The intent provided has no data associated with it")
      else:
        data = self.data[intent]
        dataFound = None
        entityCopy = copy.deepcopy(entities)

        while len(entityCopy) > 0:
          match = self.matcher.match(entityCopy, data.keys())
          if len(match) > 0:
            entityCopy.remove(match[1])
            keyToGoInto = match[0]
            data = data[keyToGoInto]
            dataFound = data
          else:
            break

        if dataFound:
          return outputStrategy(data)
        else:
          return None

      
    def aggregateTotal(self, startingPoint):
        sum = 0
        if not type(startingPoint) is dict:
            return 0
        for key in startingPoint:
            if type(startingPoint[key]) is int or type(startingPoint[key]) is float:
                sum = sum+startingPoint[key]
            else: 
                sum = sum + self.aggregateTotal(startingPoint[key])
        return sum


  
