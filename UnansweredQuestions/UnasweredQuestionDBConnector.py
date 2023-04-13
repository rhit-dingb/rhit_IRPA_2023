
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
    def addNewUnansweredQuestion(question, chatbotAnswers):
        pass

    @abstractmethod
    def getQuestionAnswerObjectById(id):
        pass

    @abstractmethod
    def deleteUnansweredQuestion(id):
       pass

    @abstractmethod
    def updateFeedbackForAnswer(self, questionId, chatbotAnswer, feedback):
        pass