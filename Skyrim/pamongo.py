from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


#setup initial connection to MongoDB cluster and DB
MONGO_DNS = MongoClient("mongodb+srv://Cermak059:Pieman1993!@cluster0-nuw5p.mongodb.net/test?retryWrites=true&w=majority")
db = MONGO_DNS["PalosTest"]
collection = db["Users"]
authCollection = db["Auth"]

def Authorization(token):
    #Find token in authCollection 
    authResults = authCollection.find_one({"Token": token})
    if not authResults:
        return None

    return authResults['Username']
