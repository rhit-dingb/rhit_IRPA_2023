from pymongo import MongoClient
from DataManager.constants import MONGO_DB_CONNECTION_STRING
from backendAPI.constants import USERNAME_FIELD_KEY
import json
from bson import json_util

class AuthenticationManager:
    def __init__(self):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        self.db = self.client["UserInfo"]   
        # insert root user
        self.db["user"].update_one({}, { "$set": { 'username': "chow", 'role': "root" } }, upsert=True)

    def getAdmins(self):
        cursor = self.db["user"].find({ "$or" : [{"role": "admin"}, {"role": "root"}]})
        admins = list(cursor)
        admins = json.loads(json_util.dumps(admins))
        print(admins)
        return admins
    
    
    # def getAdmin(self, name):
    #     return "ok"

    def checkIsAdmin(self, username):
        admins = self.getAdmins()
        print(admins)
        for adminObj in admins:
            if adminObj[USERNAME_FIELD_KEY] == username:
                return True
        return  False
        

    
