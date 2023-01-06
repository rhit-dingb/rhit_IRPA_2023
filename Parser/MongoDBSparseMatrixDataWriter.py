import json
from typing import List
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
        self.subsectionKey = "subsection"

    def writeSparseMatrix(self, sparseMatrix : SparseMatrix, sectionName : str) -> None:
        #In the parse, the subsection name of the sparse matrix is the full sheet name on the input excel file.
        # print("writing")
        
        # print(sparseMatrix.toJson)
        # sparseMatrixJsob = sparseMatrix.toJson()
        # val = json.loads(sparseMatrixJsob)
        # for row in sparseMatrix:
        #     jsonRows = row.to_json()
        #     print(jsonRows)
        jsonRows = sparseMatrix.rowsToJson()
        self.db[sectionName].update_one({self.subsectionKey : sparseMatrix.subSectionName},
        {"$set": {"rows": jsonRows, self.subsectionKey : sparseMatrix.subSectionName}}, upsert=True)


    def writeSparseMatrices(self, sparseMatrices : List[SparseMatrix], sectionName : str) -> None:
        for sparseMatrix in sparseMatrices:
            self.writeSparseMatrix(sparseMatrix, sectionName)
        #Delete all the old sparse matrix-- the one that exist in the database but was not updated or newly inserted
        subsectionsInserted = [sparseMatrix.subSectionName for sparseMatrix in sparseMatrices]
        query = { self.subsectionKey : { "$nin": subsectionsInserted } }
        self.db[sectionName].delete_many(query)
