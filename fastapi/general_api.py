from fastapi import FastAPI
from pymongo import MongoClient
import sys
from fastapi import FastAPI, Request

sys.path.append('../')
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
client = MongoClient(MONGO_DB_CONNECTION_STRING)
from fastapi.middleware.cors import CORSMiddleware
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

@app.post("/api/upload_cds_data")
async def parse_cds_data(request : Request):
    print(await request.json())




