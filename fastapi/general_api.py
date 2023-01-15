
from typing import Dict, List
from fastapi import FastAPI
from pymongo import MongoClient
import sys
sys.path.append('../')
from fastapi import FastAPI, Request, HTTPException



from DataManager.constants import CDS_DEFINITION_DATABASE_NAME

from DataManager.constants import CDS_DATABASE_NAME_TEMPLATE
from DataManager.MongoDataManager import MongoDataManager
from Parser.MongoDBSparseMatrixDataWriter import MongoDBSparseMatrixDataWriter
from Parser.ParserFacade import ParserFacade
from Parser.JsonCDSDataLoader import JsonCDSDataLoader

from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
from fastapi.middleware.cors import CORSMiddleware

mongoDbDataManager = MongoDataManager()
client = MongoClient(MONGO_DB_CONNECTION_STRING)

app = FastAPI()

#A list of allowed origins
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, this is IRPA Common Dataset API Service"}


@app.get("/api/get_all_cds_data")
async def getAllCdsData():
    cdsData = mongoDbDataManager.getAllAvailableCDSData()
    return {"data": cdsData}

"""
Example Expected json body for cds data, for definitions, there is no yearFrom and yearTo
{
    "type"
    "yearFrom": "2020",
    "yearTo": "2021",
    "data": {'General Info': 
    # [
    # {'Question': "What is Rose-Hulman's mailing address?", 'Answer': "Rose-Hulman's mailing address is 5500 Wabash Ave, Terre 
    # Haute, IN 47803", 'Complete Sentence?': 'Yes'}, 
    # {'Question': 'What is Rose-Hulman main phone number?', 'Answer': "Rose-Hulman's main phone number is (812) 877-1511", 'Complete Sentence?': 'Yes'}, 
    # {'Question': 'What is Rose-Hulman’s www home page address / website?', 'Answer': "Rose-Hulman's website is www.rose-hulman.edu", 'Complete Sentence?': 'Yes'}, 
    # .....],
   #'Enrollment_General': [.....], 
#  }
}
"""
@app.post("/api/upload_cds_data")
async def parse_cds_data(request : Request):
    print("UPLOAD DATA")
    jsonData = await request.json()
    dataType = jsonData["type"]
    excelData = jsonData["data"]
    # print(jsonData)
    jsonCdsLoader = JsonCDSDataLoader()
    outputName = ""
    if dataType ==  "annual":
        yearFrom = jsonData["yearFrom"]
        yearTo = jsonData["yearTo"]
        outputName = CDS_DATABASE_NAME_TEMPLATE.format(start_year = yearFrom, end_year = yearTo)
        
    elif dataType == "definition":
        outputName = CDS_DEFINITION_DATABASE_NAME

    if not outputName == "":
        # try:
            print(excelData)
            jsonCdsLoader.loadData(excelData)
            dataWriter = MongoDBSparseMatrixDataWriter(outputName)
            parserFacade = ParserFacade(dataLoader=jsonCdsLoader, dataWriter=dataWriter)
            await parserFacade.parse()
            return {"message": "Done"}
        # except Exception:
        #     raise HTTPException(status_code=500, detail="Something went wrong while parsing the input data")



        
    
    

@app.post("/api/get_section_and_subsection_for_cds_data")
async def parse_cds_data(request : Request):
    jsonData = await request.json()
    print("JSON DATA")
    print(jsonData)
    cdsDataName = jsonData["cdsDataName"]
    # # print(jsonData)
    sectionAndSubsections : Dict[str, List[str]] = mongoDbDataManager.getSectionAndSubsectionsForCDSData(cdsDataName)
    print(sectionAndSubsections)
    return {"data": sectionAndSubsections}





