# This is be a interface that will be implemented by concrete classes.
class KnowledgeBase:
    def __init__(self):
        pass 

    def getAvailableOptions(self, key):
        raise Exception("This method must be implemented by a class implementing this interface")


    def searchForAnswer(self, intent, entities):
        raise Exception("This method must be implemented by a class implementing this interface")