from enum import Enum

class FeedbackType(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"


class FeedbackLabel():
    
    """
    Feedback label for knowledgebase training, for one of the answer for a query
    """
    def __init__(self, query, source, answerProvided, feedback : FeedbackType, metadata):
        self.query = query
        self.answerProvided = answerProvided
        self.source = source
        self.feedback = feedback
        self.metadata = metadata