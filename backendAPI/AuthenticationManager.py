from pymongo import MongoClient
from DataManager.constants import MONGO_DB_CONNECTION_STRING

class AuthenticationManager:
    def __init__(self):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)


    def getAdmins(self):
        return ["chow", "zhengy6"]
    
    # def getAdmin(self, name):
    #     return "ok"

    def checkIsAdmin(self, username):
        admins= self.getAdmins()
        return username in admins
        

    
