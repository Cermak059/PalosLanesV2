from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


#setup initial connection to MongoDB cluster and DB
MONGO_DNS = MongoClient("mongodb+srv://Cermak059:Pieman1993!@cluster0-nuw5p.mongodb.net/test?retryWrites=true&w=majority")
db = MONGO_DNS["PalosTest"]
collection = db["Users"]
authCollection = db["Auth"]
tempCollection = db["Temp"]
pendingReset = db["Reset"]
bogoCollection = db["BOGO"]
freeCollection = db["FREEGAME"]
        
def Authorization(token):
    authResults = authCollection.find_one({"Token": token})
    if not authResults:
        return None

    return authResults['Username']

def resetAuth(token):
    authResults = pendingReset.find_one({"Token": token})
    if not authResults:
        return None

    return authResults['Email']



        
