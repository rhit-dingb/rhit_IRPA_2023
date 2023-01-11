import json
from typing import Dict, List
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from Parser.SparseMatrixDataWriter import SparseMatrixDataWriter
from Data_Ingestion.SparseMatrix import SparseMatrix
from pymongo import MongoClient



class MongoDBSparseMatrixDataWriter(SparseMatrixDataWriter):
    #database name can be existing database or a new one
    def __init__(self, outputName):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        print("CONNECTED")
        self.databaseName = outputName
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


    # def writeSparseMatrices(self, sparseMatrices : List[SparseMatrix], sectionName : str) -> None:
        
    

    def writeSparseMatrices(self, sectionToSparseMatrices : Dict[str, List[SparseMatrix]]): 
        sectionsInserted = []
        for section in sectionToSparseMatrices:
            sparseMatrices = sectionToSparseMatrices[section]
            for sparseMatrix in sparseMatrices:
                self.writeSparseMatrix(sparseMatrix, section)
                #Delete all the old sparse matrix-- the one that exist in the database but was not updated or newly inserted
                subsectionsInserted = [sparseMatrix.subSectionName for sparseMatrix in sparseMatrices]
                # Delete any documents for subsection that is not inserted.
                query = { self.subsectionKey : { "$nin": subsectionsInserted } }
                self.db[section].delete_many(query)
            sectionsInserted.append(section)

        #Drop any section that is not in the uploaded excel file
        collections =  self.db.list_collection_names()
        for collection in collections:
            if not collection in sectionsInserted:
                self.db[collection].drop()


         

            
                