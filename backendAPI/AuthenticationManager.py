from pymongo import MongoClient
from DataManager.constants import MONGO_DB_CONNECTION_STRING

class AuthenticationManager:
    def __init__(self):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)


    def login(self, username, password):
        # hard code for now
        if username == "admin" and password == "admin123":
            return True
        

    
