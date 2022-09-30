# This is be a interface that will be implemented by concrete classes.
class KnowledgeBase:
    def __init__(self):
         raise Exception("This class serves as an interface and cannot be instantiated")

    def getAvailableOptions(self, key):
        raise Exception("This method must be implemented by a class implementing this interface")


    def searchForAnswer(self, intent, entities):
        raise Exception("This method must be implemented by a class implementing this interface")

    # this function will drill down to the numerical value givien a starting point and add up all the numbers 
    def aggregateTotal(self, startingPoint):
        raise Exception("This method must be implemented by a concrete class")
        