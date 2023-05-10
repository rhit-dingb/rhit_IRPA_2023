from typing import Dict, List


class Expression():
    """
    Abstract class representing an expression in a template
    
    """
    def __init__(self, value : str, childrenExpression ):

        """
        :param value: The raw expression string in the template
        :param childExpression: A list of Expression instances that represents the child expression of the current expression object.
        """
        self.value = value
        self.childrenExpression = childrenExpression

    
    def evaluate(entities : List[Dict[str, str]] , realAnswerEntities : List[Dict[str, str]] ,answer : str) -> str:
        """
        Abstract method. Concrete implementation of this function would evaluate the expression and return a 
        string value, or empty string if some condition is not met


        """
        raise Exception("please implement this with a concrete subclass")

        