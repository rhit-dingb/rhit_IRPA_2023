import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.mflix
collection = db.Comments
cursor = collection.find({"name": "Andrea Le"})
for doc in cursor:
    print(doc)
