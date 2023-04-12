from typing import Tuple
from DataManager.DataManager import DataManager
import redis
import pickle
from Data_Ingestion.TopicData import TopicData
from backendAPI.helper import getStartAndEndYearFromDataName
import re

class Cache(DataManager):
    def __init__(self, dataSource : DataManager):
        self.dataSource  = dataSource
        self.connected = True
        self.pool = None
        self.redis = None
        self.redisDataKeyFormat = "{intent}:{startYear}:{endYear}:{subsection}"
        try:
            self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            self.redis = redis.Redis(connection_pool=self.pool)
        except Exception:
            self.connected = False
            
    def clearCache(self):
        if self.connected:
            print("DELETING ALL KEYS")
            try:
                keys = self.redis.keys('*')
                if len(keys) > 0:
                    self.redis.delete(*keys)
            except Exception:
                self.connected = False

    
    async def getDataBySection(self, section, exceptionToThrow, startYear = None, endYear =None ) -> TopicData:
        section = section.replace("_", " ")
    
        # if section == "definition":
        #     startYear = ""
        #     endYear =  ""

        # if startYear == None:
        #     startYear = ""
        
        # if endYear == None:
        #     endYear == ""
    
        does_exist = True
        topicData = None
        subsectionsForSection = self.dataSource.getAllSubsectionForSection(section, startYear, endYear)

        if self.connected:
            for subsection in subsectionsForSection: 
                dataKey = self.redisDataKeyFormat.format(intent=section, startYear=startYear, endYear=endYear, subsection=subsection)
                try:
                    does_exist = does_exist and self.redis.exists(dataKey)
                except Exception:
                    self.connected = False
                    does_exist = False
                    break
        else:
            does_exist = False

        if does_exist:
           print("CACHE HIT")
           topicData = self.getDataFromCache(section, startYear, endYear)
        else:
           print("CACHE MISS")
           topicData = await self.getDataAndPopulateCache(section,exceptionToThrow, startYear, endYear)
                
        return topicData


    def getDataFromCache(self, section, startYear = None, endYear= None):

        topicData = TopicData(section)
        subsectionsForSection = self.getAllSubsectionForSection(section, startYear, endYear)

        
        if startYear == None:
            startYear = ""

        if endYear == None:
            endYear = ""

        for subsection in subsectionsForSection: 
            
            dataKey = self.redisDataKeyFormat.format(intent=section, startYear=startYear, endYear=endYear, subsection=subsection)
            data=self.redis.get(dataKey)
            #lets assume the data is always sparse matrix for now.
            deserializedSparseMatrix = pickle.loads(data)
            topicData.addSparseMatrix(subsection, deserializedSparseMatrix)
        return topicData


    async def getDataAndPopulateCache(self, section, exceptionToThrow, startYear = None, endYear = None, ):
        topicData : TopicData = await self.dataSource.getDataBySection(section,exceptionToThrow,startYear, endYear)
        # print(intent)
        # print(topicData.sparseMatrices.keys())
        # print("_________________")
        subsectionsForSection = self.getAllSubsectionForSection(section, startYear, endYear)

        if startYear == None or endYear == None:
            startYear = ""
            endYear = ""
            
        for subsection in subsectionsForSection: 
            dataKey = self.redisDataKeyFormat.format(intent=section, startYear=startYear, endYear=endYear, subsection=subsection)
            #lets assume the data is always sparse matrix for now.
            sparseMatrix =  topicData.getSparseMatrix(subsection)
            if sparseMatrix == None:
                continue
            
            if self.redis == None or not self.connected:
                # print("REDIS NOT CONNECTED")
                continue

            serializedSparseMatrix = pickle.dumps(sparseMatrix)

            try:
                self.redis.set(dataKey, serializedSparseMatrix )
            except Exception:
                self.connected = False
                # print("Setting key failed")

        return topicData

    def getAllAvailableData(self, regex : re.Pattern):
        return self.dataSource.getAllAvailableData(regex)


    def getAvailableOptions(self, intent,startYear, endYear):
        return self.dataSource.getAvailableOptions( intent, startYear, endYear)

    def getMostRecentYearRange(self) -> Tuple[str, str]:
        return self.dataSource.getMostRecentYearRange()
    
    def getAllAvailableYearsSorted(self):
        return self.dataSource.getAllAvailableYearsSorted()
    
    def deleteData(self, dataName) -> bool:
    
        sectionsAndSubsections = self.dataSource.getSectionAndSubsectionsForData(dataName)
        startYear, endYear = getStartAndEndYearFromDataName(dataName)

        for key in sectionsAndSubsections:
            subsections = sectionsAndSubsections[key]
            for subsection in subsections:
                dataKey = self.redisDataKeyFormat.format(intent=key, startYear=startYear, endYear=endYear, subsection=subsection)
                if self.redis == None or not self.connected:
                    print("DELETING KEY FAILED, REDIS NOT CONNECTED")
                    continue
                try:
                    self.redis.delete(dataKey)
                except Exception:
                    self.connected = False
                    print("DELETING KEY Failed")

        return self.dataSource.deleteData(dataName)


    def getAllSubsectionForSection(self, section, startYear, endYear, filter=lambda x: True):
        return self.dataSource.getAllSubsectionForSection(section, startYear, endYear, filter)
    
    def getSectionAndSubsectionsForData(self, dataName, filter=lambda x: True):
        return self.dataSource.getSectionAndSubsectionsForData(dataName, filter)
    
    def getAvailableDataForSpecificYearRange(self, startYear, endYear):
        return self.dataSource.getAvailableDataForSpecificYearRange(startYear, endYear)

  
    def getSections(self, dataName):
        return self.dataSource.getSections(dataName)
    

    def findAllYearAngosticDataName(self):
        return self.dataSource.findAllYearAngosticDataName()