import json
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from Data_Ingestion.SparseMatrix import SparseMatrix
from pymongo import MongoClient



class MongoDBSparseMatrixDataWriter(SparseMatrixDataWriter):
    #database name can be existing database or a new one
    def __init__(self, year):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        print("CONNECTED")
        self.databaseName =  DATABASE_PRENAME+str(year) + "_" + str(year+1)
        self.db = self.client[self.databaseName]

    def writeSparseMatrix(self, sparseMatrix : SparseMatrix) -> None:
        #In the parse, the subsection name of the sparse matrix is the full sheet name on the input excel file.
        print("writing")
        fullNameWithSectionAndSubsection : str = sparseMatrix.subSectionName
        sectionAndSubSection = fullNameWithSectionAndSubsection.split("_")
        section = sectionAndSubSection[0]
        subSection = sectionAndSubSection[len(sectionAndSubSection)-1]
        # print(sparseMatrix.toJson)
        # sparseMatrixJsob = sparseMatrix.toJson()
        # val = json.loads(sparseMatrixJsob)
        # for row in sparseMatrix:
        #     jsonRows = row.to_json()
        #     print(jsonRows)
        jsonRows = sparseMatrix.rowsToJson()
        self.db[section].update_one({}, {"$set": {subSection:jsonRows}}, upsert=True)

