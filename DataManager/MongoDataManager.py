from typing import Dict, List, Tuple
from DataManager.DataManager import DataManager
from Data_Ingestion.ConvertToSparseMatrixDecorator import ConvertToSparseMatrixDecorator
from Data_Ingestion.MongoProcessor import MongoProcessor
from Data_Ingestion.SparseMatrix import SparseMatrix
from Data_Ingestion.TopicData import TopicData
from Exceptions.ExceptionMessages import NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT
from Exceptions.NoDataFoundException import NoDataFoundException
from Exceptions.NotEnoughInformationException import NotEnoughInformationException
from Exceptions.ExceptionTypes import ExceptionTypes
import re
from pymongo import MongoClient

from DataManager.constants import CDS_DATABASE_NAME_TEMPLATE, DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from DataManager.constants import DATABASE_SUBSECTION_FIELD_KEY
from DataManager.constants import ANNUAL_DATA_REGEX_PATTERN
from DataManager.constants import DEFINITION_DATA_REGEX_PATTERN
from DataManager.constants import DATABASE_METADATA_FIELD_KEY
from Data_Ingestion.constants import ABOUT_METADATA_KEY
from Parser.RasaCommunicator import RasaCommunicator
from Data_Ingestion.SubsectionQnA import SubsectionQnA
"""
MongoDataManager subclass that can handle connections with MongoDB data
"""
class MongoDataManager(DataManager):
    def __init__(self, mongoProcessor):
        super().__init__()
        # self.mongoProcessor = MongoProcessor()
        # self.mongoProcessor = ConvertToSparseMatrixDecorator(self.mongoProcessor)
        self.mongoProcessor : MongoProcessor = mongoProcessor
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        self.rasaCommunicator = RasaCommunicator()


    def findDefinitionData(self):
        patternDefinition = re.compile(DEFINITION_DATA_REGEX_PATTERN, re.IGNORECASE)
        definitionDatabasesNames = self.getAllAvailableData(patternDefinition)
        return definitionDatabasesNames
    
     
    def findAllYearAngosticDataName(self):
        # only find defintion for now, but probably later wil change
        return self.findDefinitionData()
       
    def getAvailableOptions(self, intent, startYear, endYear):
        availableOptions = dict() 
        definitionDatabaseNames = self.findDefinitionData()
        annualDatabaseNames = self.getAvailableDataForSpecificYearRange(startYear, endYear)
        databaseNames = annualDatabaseNames+ definitionDatabaseNames

        for databaseName in databaseNames:
            if databaseName in self.client.list_database_names():
                db = self.client[databaseName]
                collections = db.list_collection_names()
                for collection in collections:
                    # print(collection)
                    cursor = db[collection].find({},{DATABASE_METADATA_FIELD_KEY:1})
                    for data in cursor:
                        if not collection in availableOptions.keys():
                            availableOptions[collection] = []

                        if not DATABASE_METADATA_FIELD_KEY in data:
                            continue
                        metadata = data[DATABASE_METADATA_FIELD_KEY]
                        if ABOUT_METADATA_KEY in metadata:
                            aboutDescription = metadata[ABOUT_METADATA_KEY]
                            availableOptions[collection].append(aboutDescription)
        if intent == None:
            intent = ""
                                
        intent = intent.replace("_", " ") 

        if intent in availableOptions:
            newDict = dict()
            newDict[intent] = availableOptions[intent]
            return newDict

        return availableOptions



    def getAllSubsectionForSection(self, section, startYear = None, endYear = None, filter = lambda x: True):
        subsectionForSection = []
        dataNames = []
        #might refactor this later
        if startYear == None or endYear == None:
            dataNames = self.findDefinitionData()
        else:
            dataNames = self.getAvailableDataForSpecificYearRange(startYear, endYear)

        
        def filter(collection):
            return collection == section
        for databaseName in dataNames:
           sectionToSubSection = self.getSectionAndSubsectionsForData(databaseName, filter=filter)
           if section in sectionToSubSection:
               subsectionForSection = subsectionForSection+sectionToSubSection[section]

        return subsectionForSection



    def getSectionAndSubsectionsForData(self, dataName, filter=lambda x: True) -> Dict[str, List[str]] :
        sectionToSubections = dict()
        databases = self.client.list_database_names()
        for databaseName in databases: 
            if dataName == databaseName:
                db = self.client[databaseName]
                sections = self.getSections(dataName)
                for collection in sections:
                    if not filter(collection):
                        continue
                    subsectionsData = db[collection].find({}, {DATABASE_SUBSECTION_FIELD_KEY :1})
                    for subsection in subsectionsData:
                      
                        if not DATABASE_SUBSECTION_FIELD_KEY in subsection:
                            continue
                        subSectionName = subsection[DATABASE_SUBSECTION_FIELD_KEY]
                        if collection in sectionToSubections:
                            sectionToSubections[collection].append(subSectionName)
                        else:
                            sectionToSubections[collection] = [subSectionName]
                            
        # sort the keys and array
        keys = list(sectionToSubections.keys())
        keys.sort()
        sortedDict = dict()

        for key in keys:
            subsections = sectionToSubections[key]
            # subsections.sort()
            sortedDict[key] = subsections

        return sortedDict
    


    def deleteData(self, dataName) -> bool:
        if dataName in self.client.list_database_names():
            self.client.drop_database(dataName)
            return True
        else:
            return False

    def getAllAvailableData(self, regex : re.Pattern):
        databases = self.client.list_database_names()
        availableData = []
        # print(databases)
        for database in databases: 
            didMatch = regex.match(database.lower())
            if didMatch:
                availableData.append(database)
        
        return availableData
    
    def getAvailableDataForSpecificYearRange(self,startYear, endYear) -> List[str]:
        patternYear = re.compile(".+"+str(startYear)+"."+str(endYear), re.IGNORECASE)
        databasesAvailableForGivenYear = self.getAllAvailableData(patternYear)
        return databasesAvailableForGivenYear


    def getSections(self, dataName):
        return self.client[dataName].list_collection_names()


    async def getDataBySection(self, section, exceptionToThrow: Exception,  startYear= None, endYear = None):
            section =  section.replace("_", " ")
            selectedDatabaseName = ""
            databaseNames = []
            if startYear == None or endYear == None:
                databaseNames = self.findAllYearAngosticDataName()
                if len(databaseNames) == 0:
                    raise exceptionToThrow
                
            else: 
                databaseNames = self.getAvailableDataForSpecificYearRange(startYear, endYear)
                if len(databaseNames) == 0:
                    raise exceptionToThrow


            for databaseName in databaseNames:
                    sections = self.getSections(databaseName)
                    if section in sections:
                        selectedDatabaseName = databaseName

            if selectedDatabaseName == "":
                raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = section, start= startYear, end=endYear), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
            
            convertedDataModel = await self.mongoProcessor.getDataByDbNameAndSection(self.client, section, selectedDatabaseName)     
            return convertedDataModel

    """
    See documentation in DataManager.py
    """
    def getMostRecentYearRange(self) -> Tuple[str, str] :
        years = self.getAllAvailableYearsSorted()
        if len(years) == 0:
            raise Exception("No data found in database")

        mostRecentYearRange = years[0]
        # print(mostRecentYearRange)
        return years[0]


    def getAllAvailableYearsSorted(self) -> List[Tuple[str,str]]:
        def sortFunc(year):
            startYear= year[1]
            return startYear


        dbNameWithYears = self.client.list_database_names()
        pattern = re.compile(ANNUAL_DATA_REGEX_PATTERN, re.IGNORECASE)
        dbNameWithYears = list(filter(lambda x : pattern.match(x), dbNameWithYears))
        years = []
        for name in dbNameWithYears:
            nameSplitted = name.split("_")
            yearRange = nameSplitted[1:]
            if not yearRange in years:
                years.append((yearRange[0], yearRange[1]))

        years.sort(key = sortFunc, reverse= True)
        return years



# -----------The following are Unit Tests for the MongoDataManager Class
# NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT = "Sorry I could not find any data for academic year {start}-{end}"
# exceptionToThrow = NoDataFoundException(NO_DATA_FOUND_FOR_ACADEMIC_YEAR_ERROR_MESSAGE_FORMAT.format(start=2020, end=2021), ExceptionTypes.NoDataFoundForAcademicYearException)
# manager = MongoDataManager()
# manager.getSparseMatricesByStartEndYearAndIntent(["enrollment"],2020,2021,exceptionToThrow)
