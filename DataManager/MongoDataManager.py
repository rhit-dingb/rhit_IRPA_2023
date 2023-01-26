from typing import Dict, List, Tuple
from DataManager.DataManager import DataManager
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
"""
MongoDataManager subclass that can handle connections with MongoDB data
"""
class MongoDataManager(DataManager):
    def __init__(self):
        super().__init__()
        self.mongoProcessor = MongoProcessor()
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)

    def getAvailableOptions(self, intent, startYear, endYear):
        # allAvailableYears = self.getAllAvailableYearsSorted(self)
        # yearRange = (startYear, endYear)
        availableOptions = dict() 
        databaseName = CDS_DATABASE_NAME_TEMPLATE.format(start_year = startYear, end_year = endYear)
        # print("DATABASE NAME", databaseName)
        if databaseName in self.client.list_database_names():
            db = self.client[databaseName]
            collections = db.list_collection_names()
            for collection in collections:
                # print(collection)
                cursor = db[collection].find({},{DATABASE_METADATA_FIELD_KEY:1})
                for data in cursor:
                    # print(data)
                    metadata = data[DATABASE_METADATA_FIELD_KEY]
                    print(metadata)
                    if ABOUT_METADATA_KEY in metadata:
                        aboutDescription = metadata[ABOUT_METADATA_KEY]
                        if not collection in availableOptions.keys():
                            availableOptions[collection] = [aboutDescription]
                        else:
                            print(collection)
                            print(availableOptions.keys())
                            availableOptions[collection].append(aboutDescription)

        print("AVIALABLE OPTIONS FOUND")
        print(availableOptions)
        return availableOptions
                # print(list(cursor))


    def getSectionAndSubsectionsForData(self, dataName) -> Dict[str, List[str]] :
        sectionToSubections = dict()
        databases = self.client.list_database_names()
        for databaseName in databases: 
            if dataName == databaseName:
                db = self.client[databaseName]
                collections = db.list_collection_names()
                for collection in collections:
                    subsectionsData = db[collection].find({}, {DATABASE_SUBSECTION_FIELD_KEY :1})
                    for subsection in subsectionsData:
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
            # print("_______-")
            # print(regex)
            # print(database.lower())
            # print(didMatch)
            if didMatch:
                # print("MATCHED WITH", database)
                # print(regex)
                availableData.append(database)
        
        return availableData


    def getSections(self, dataName):
        return self.client[dataName].list_collection_names()

    

    """
    See documentation in DataManager.py
    """
    def getSparseMatricesByStartEndYearAndIntent(self, intent, start, end, exceptionToThrow: Exception) -> TopicData:
            # cdsDatabase = CDS_DATABASE_NAME_TEMPLATE.format(start_year= start, end_year = end)
            # if not cdsDatabase in self.client.list_database_names():
            #     raise exceptionToThrow

            patternYear = re.compile(".+"+str(start)+"."+str(end), re.IGNORECASE)
            patternDefinition = re.compile(DEFINITION_DATA_REGEX_PATTERN)
            definitionDatabases = self.getAllAvailableData(patternDefinition)
            databasesAvailableForGivenYear = self.getAllAvailableData(patternYear)
            
            if len(databasesAvailableForGivenYear) == 0:
                raise exceptionToThrow

            intent = intent.replace("_", " ")
            selectedDatabaseName = ""
            for databaseName in databasesAvailableForGivenYear:
                sections = self.getSections(databaseName)
                if intent in sections:
                    selectedDatabaseName = databaseName

            # We expect there to be only one definition data
            if selectedDatabaseName == "":
                definitionSections = self.getSections(definitionDatabases[0])
                if len(definitionDatabases) > 0:
                    if intent in definitionSections:
                        selectedDatabaseName = definitionDatabases[0]

            if selectedDatabaseName == "":
                raise NoDataFoundException(NO_DATA_AVAILABLE_FOR_GIVEN_INTENT_FORMAT.format(topic = intent, start= start, end=end), ExceptionTypes.NoSparseMatrixDataAvailableForGivenIntent)
        
            topicData = self.mongoProcessor.getSparseMatricesByDbNameAndIntent(self.client, intent, selectedDatabaseName)
            print("TOPIC DATA")
            print(topicData)
            # cursor = topicData.find()
            # for doc in cursor:
            #     print(doc)           
            return topicData

    """
    See documentation in DataManager.py
    """
    def getMostRecentYearRange(self) -> Tuple[str, str] :
        years = self.getAllAvailableYearsSorted()
        if len(years) == 0:
            raise Exception("No data found in database")

        mostRecentYearRange = years[0]
        print(mostRecentYearRange)
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
