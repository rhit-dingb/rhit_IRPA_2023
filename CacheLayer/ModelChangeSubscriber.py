from typing import Dict
from CacheLayer.Cache import Cache
from CacheLayer.EventSubscriber import EventSubscriber
from CacheLayer.EventType import EventType


class ModelChangeSubscriber(EventSubscriber):
    def __init__(self, eventType : EventType, cache : Cache ):
        super().__init__(eventType)
        self.cache = cache

    async def notify(self, eventData : Dict[str, any]):
        self.cache.clearCache()