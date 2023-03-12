
from typing import Dict
from CacheLayer.Cache import Cache

from CacheLayer.CacheEventPublisher import EventType
from CacheLayer.EventSubscriber import EventSubscriber
from CacheLayer.constants import END_YEAR_KEY, SECTIONS_UPLOADED_KEY, START_YEAR_KEY
from Exceptions.ExceptionMessages import NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT
from Exceptions.ExceptionTypes import ExceptionTypes
from Exceptions.NoDataFoundException import NoDataFoundException
class DataUploadSubscriber(EventSubscriber):
    def __init__(self, eventType : EventType, cache : Cache ):
        super().__init__(eventType)
        self.cache = cache


    async def notify(self, eventData : Dict[str, any]):
        sectionsUploadedKey = SECTIONS_UPLOADED_KEY
        startYearKey = START_YEAR_KEY 
        endYearKey = END_YEAR_KEY 
        # if subsectionsUploadedKey in eventData:
        sectionsUploaded = eventData[sectionsUploadedKey]
        startYear = ""
        endYear = ""
        if startYearKey in eventData and endYearKey in eventData:
            startYear = eventData[startYearKey]
            endYear = eventData[endYearKey]
        exceptionToThrow = NoDataFoundException(NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=startYear, end=endYear), ExceptionTypes.NoDataFoundForAcademicYearException)
        for sectionUploaded in sectionsUploaded:
            #Repopulate cache
            await self.cache.getDataAndPopulateCache(sectionUploaded, startYear, endYear, exceptionToThrow)