from typing import Tuple
from DataManager.DataManager import DataManager
import redis
import pickle
from Data_Ingestion.TopicData import TopicData

class Cache(DataManager):
    def __init__(self, dataSource : DataManager):
        self.dataSource  = dataSource
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.redis = redis.Redis(connection_pool=self.pool)

    
    async def getDataByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow) -> TopicData:
        intent = intent.replace("_", " ")
        redisDataKeyFormat = "{intent}:{startYear}:{endYear}:{subsection}"
        # redisDataKey = intent+"_"+"start"+"end"
        # does_exist = self.redis.exists(redisDataKey)
        does_exist = True
        topicData = None
        subsectionsForSection = self.dataSource.getAllSubsectionForSection(intent, start, end)
    
        for subsection in subsectionsForSection: 
            dataKey = redisDataKeyFormat.format(intent=intent, startYear=start, endYear=end, subsection=subsection)
            does_exist = does_exist and self.redis.exists(dataKey)

        if does_exist:
            topicData = TopicData(intent)
            print("INSIDE CACHE")
            for subsection in subsectionsForSection: 
                dataKey = redisDataKeyFormat.format(intent=intent, startYear=start, endYear=end, subsection=subsection)
                data=self.redis.get(dataKey)
                #lets assume the data is always sparse matrix for now.
                deserializedSparseMatrix = pickle.loads(data)
                topicData.addSparseMatrix(subsection, deserializedSparseMatrix)
        else:
            topicData : TopicData = await self.dataSource.getDataByStartEndYearAndIntent(intent, start, end, exceptionToThrow)
            print("NOT IN CACHE")
            # print(intent)
            # print(topicData.sparseMatrices.keys())
            # print("_________________")
            for subsection in subsectionsForSection: 
                dataKey = redisDataKeyFormat.format(intent=intent, startYear=start, endYear=end, subsection=subsection)
                #lets assume the data is always sparse matrix for now.
                sparseMatrix =  topicData.getSparseMatrix(subsection)
                if sparseMatrix == None:
                    continue
                serializedSparseMatrix = pickle.dumps(sparseMatrix)
                self.redis.set(dataKey, serializedSparseMatrix )
                
        return topicData


    def getAvailableOptions(self,startYear, endYear):
        return self.dataSource.getAvailableOptions(startYear, endYear)

    def getMostRecentYearRange(self) -> Tuple[str, str]:
        return self.dataSource.getMostRecentYearRange()
    

    def deleteData(self, dataName) -> bool:
        self.dataSource.deleteData(dataName)