
from typing import Dict
from CacheLayer.Cache import Cache

from CacheLayer.CacheEventPublisher import EventType
from CacheLayer.EventSubscriber import EventSubscriber
from CacheLayer.constants import DATA_DELETED_KEY
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.NoDataFoundException import NoDataFoundException
class DataDeletionSubscriber(EventSubscriber):
    def __init__(self, eventType : EventType, cache : Cache ):
        super().__init__(eventType)
        self.cache = cache

    

    async def notify(self, eventData : Dict[str, any]):
        # print(eventData)
        dataToDeleteKey = DATA_DELETED_KEY
        dataToDelete = eventData[dataToDeleteKey]
        self.cache.deleteData(dataToDelete)
     