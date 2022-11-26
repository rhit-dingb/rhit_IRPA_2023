# This is be a interface that will be implemented by concrete classes.
from copy import deepcopy
from Knowledgebase.DefaultShouldAddRow import DefaultShouldAddRowStrategy
from Knowledgebase.ShouldAddRowStrategy import ShouldAddRowStrategy


class KnowledgeBase:
    def __init__(self):
        raise Exception("This class serves as an interface and cannot be instantiated")

    def getAvailableOptions(self, key):
        raise Exception("This method must be implemented by a class implementing this interface")

    def searchForAnswer(self, intent, entities):
        raise Exception("This method must be implemented by a class implementing this interface")

    # this function will aggregate number given a range, using the generator to create column name for those rows and 
    # sum up the value for those rows
    def aggregateDiscreteRange(self, intent, filteredEntities, start, end, generator):
        raise Exception("This method must be implemented by a class implementing this interface")

    def aggregatePercentage(self, intent, numerator, entitiesToCalculateDenominator):
        raise Exception("This method must be implemented by a class implementing this interface")
