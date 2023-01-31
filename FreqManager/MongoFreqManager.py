from abc import ABC, abstractmethod
from enum import Enum

class Observer(ABC):
    """
    The Observer class defines an updating interface for objects that
    should be notified of changes in a subject.
    """
    @abstractmethod
    def update(self):
        pass

class UserEventSubject:
    """
    The Subject class maintains a list of observers and provides an
    interface for attaching and detaching observers.
    """
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()

class GeneralStatsObserver(Observer):
    """
    This class monitor how many question is asked, when the user is happy with the result
    """

class UserFeedback(Enum):
    NO_FEEDBACK = 1
    HELPFUL = 2
    NOT_HELPFUL = 3

class QuestionCategory(Enum):
    ENROLLMENT = 1
    ADMISSION = 2
    HIGH_SCHOOL_UNITS = 3
    BASIS_FOR_SELECTION = 4
    
