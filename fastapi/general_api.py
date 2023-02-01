from fastapi import FastAPI
from pymongo import MongoClient
import sys
sys.path.append('../')
from DataManager.constants import DATABASE_PRENAME, MONGO_DB_CONNECTION_STRING
client = MongoClient(MONGO_DB_CONNECTION_STRING)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, this is IRPA Common Dataset Database Service"}
