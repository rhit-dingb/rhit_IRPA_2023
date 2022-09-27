
#Class to match an entity with a key in the knowledgebase to determine if they match
class Matcher:
    def __init__(self):
        raise Exception("This class serves as an interface and cannot be instantiated")


    def match(self, key, entity) -> bool:
        raise Exception("This method must be implemented by a class implementing this interface")