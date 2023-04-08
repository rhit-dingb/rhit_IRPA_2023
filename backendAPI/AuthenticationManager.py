from pymongo import MongoClient
from DataManager.constants import MONGO_DB_CONNECTION_STRING
from backendAPI.constants import USERNAME_FIELD_KEY
import json
from bson import json_util
from decouple import config

class AuthenticationManager:
    def __init__(self):
        self.client = MongoClient(MONGO_DB_CONNECTION_STRING)
        self.db = self.client["UserInfo"]   
        # insert root user
        rootUser = config('ROOT_USERNAME')
        self.db["user"].update_one({"username":rootUser}, { "$set": { 'username': rootUser, 'role': "root" } }, upsert=True)

    def getAdmins(self):
        cursor = self.db["user"].find({ "$or" : [{"role": "admin"}, {"role": "root"}]})
        admins = list(cursor)
        admins = json.loads(json_util.dumps(admins))
        print(admins)
        return admins
    
    def addAdmin(self, currentUser, usernameToAdd):
        isRoot = self.checkIsRoot(currentUser)
        if isRoot:
            self.addUser(usernameToAdd, "admin")

    def transferRootAcess(self,transferFrom, transferTo) -> bool:
        isRoot = self.checkIsRoot(transferFrom)
        if not isRoot:
            return False
        
        userData = self.getUserData(transferTo)
        if not userData or not userData["role"] == "admin" :
            return False

        self.db["user"].update_one({"username":transferFrom}, { "$set": {  'role': "admin" } })
        self.db["user"].update_one({"username":transferTo}, { "$set": {'role': "root" } }, upsert=True)
        return True


    def addUser(self, username, role):
        userData = self.getUserData(username)
        if userData == None:
            print("INSERTING", username)
            self.db["user"].insert_one({"username":username, "role": role})

    
    def getUserData(self, username):
        data= self.db["user"].find_one({"username": username})
       
        if data:
            result=  json.loads(json_util.dumps(data))
          
            return result
        else:
            return None
        

    def deleteUser(self, currentUser, usernameToDelete):
        # print("DELETING", username)
        isRoot = self.checkIsRoot(currentUser)
        if isRoot:
            self.db["user"].delete_one({"username": usernameToDelete})
    

    def checkIsAdmin(self, username):
        admins = self.getAdmins()
        print(admins)
        for adminObj in admins:
            if adminObj[USERNAME_FIELD_KEY] == username:
                return True
        return  False
        

    def checkIsRoot(self, username):
        userData = self.getUserData(username)
        if userData == None:
            return False
        else:
            if userData["role"] == "root":
                return True
            else: 
                return False

    
