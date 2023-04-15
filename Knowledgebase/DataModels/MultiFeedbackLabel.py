from typing import List

from Knowledgebase.DataModels.FeedbackLabel import FeedbackLabel


class MultiFeedbackLabel():
    """
    Data model class to contain the list of feedback label for each of the answer for one query.
    """
    def __init__(self, query, feedbackLabels : List[FeedbackLabel]):
        self.query = query
        self.feedbackLabels = feedbackLabels


    