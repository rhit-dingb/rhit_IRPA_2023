from abc import ABC, abstractmethod
from typing import Dict

from CacheLayer.EventType import EventType

class EventSubscriber(ABC):
    def __init__(self, eventType : EventType):
        self.eventType = eventType

    
    def isEventType(self, eventType):
        return eventType == self.eventType
    
    @abstractmethod
    async def notify(self, eventData : Dict[str, any]):
        pass
