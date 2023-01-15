from pymongo import MongoClient, InsertOne
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client.freq_question_db
collection = db.unans_question

# document = {
#     "_id": ObjectId("63c47ffbda6609c3dd3b3847"),
#     "content": "Sample 1: testing purpose",
#     "post_date": datetime(2023, 1, 13),
#     "is_addressed": False,
#     "answer": None
# }

# collection.insert_one(document)

documents = [
    {
        "_id": ObjectId("63c47ffbda6609c3dd3b3847"),
        "content": "Sample 1: testing purpose",
        "post_date": datetime(2023, 1, 13),
        "is_addressed": False,
        "answer": None
    },
    {
        "_id": ObjectId("63c47ffbda6609c3dd3b3848"),
        "content": "Sample 2: testing purpose",
        "post_date": datetime(2023, 1, 13),
        "is_addressed": False,
        "answer": None
    },
    {
        "_id": ObjectId("63c47ffbda6609c3dd3b3849"),
        "content": "Sample 3: testing purpose",
        "post_date": datetime(2023, 1, 13),
        "is_addressed": False,
        "answer": None
    },
    {
        "_id": ObjectId("63c47ffbda6609c3dd3b3850"),
        "content": "Sample 4: testing purpose",
        "post_date": datetime(2023, 1, 13),
        "is_addressed": False,
        "answer": None
    },
    {
        "_id": ObjectId("63c47ffbda6609c3dd3b3851"),
        "content": "Sample 5: testing purpose",
        "post_date": datetime(2023, 1, 13),
        "is_addressed": False,
        "answer": None
    }
]

collection.insert_many(documents)

