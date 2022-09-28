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
        sum = 0
        if not type(startingPoint) is dict:
            return 0
        for key in startingPoint:
            if type(startingPoint[key]) is int or type(startingPoint[key]) is float:
                sum = sum+startingPoint[key]
            else: 
                sum = sum + self.aggregateTotal(startingPoint[key])
        return sum