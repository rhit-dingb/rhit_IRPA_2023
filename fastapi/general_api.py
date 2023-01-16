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

# General API for getting unanswered questions
@app.get("/questions")
async def get_unans_questions():
    db = client.freq_question_db
    questions_collection = db.unans_question
    unanswered_questions = list(questions_collection.find({"is_addressed": False}))
    return unanswered_questions