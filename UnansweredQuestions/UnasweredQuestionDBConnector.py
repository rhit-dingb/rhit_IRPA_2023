
from abc import ABC, abstractmethod
class UnansweredQuestionDbConnector(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getAllUnansweredQuestionAndAnswer(self):
        pass

    @abstractmethod
    def getAnsweredQuestionSortedByDate(self):
        pass

    @abstractmethod
    def provideAnswerToUnansweredQuestion(questionId):
        pass

    @abstractmethod
    def addNewUnansweredQuestion(question):
        pass

    