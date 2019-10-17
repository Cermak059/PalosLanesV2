from flask import Flask, request
from flask_restplus import Api, Resource
from passlib.hash import sha256_crypt
import json
import re
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from paschema import UserSchema
from pacrypto import EncryptPassword, \
                     VerifyPassword

app = Flask(__name__)
api = Api(app)

#setup initial connection to MongoDB cluster and DB
client = MongoClient("mongodb+srv://Cermak059:Pieman1993!@cluster0-nuw5p.mongodb.net/test?retryWrites=true&w=majority")
db = client["PalosTest"]
collection = db["Users"]


class Register(Resource):
    def post(self):

        #Instantiate schema and load requested data into dictionary
        schema = UserSchema()
        data=json.loads(request.data)

        #Create new user by loading data from dictionary into UserSchema
        new_user = schema.load(data)

        #Now validate formatting of user data with validate_Data method
        UserSchema.validate_Data(new_user)

        #Check to see if username is taken
        if collection.find_one({"Username": new_user['Username']}):
            raise ValueError("Username already taken please try again")

        #Check if user exists in DB
        if collection.find_one({"Email": new_user['Email']}):
            print("You already have an account")
        else:
            collection.insert_one(new_user)
            print ("User added")


class Login(Resource):
     def post(self):
          #Instantiate schema and load login data into dictionary
          schema = UserSchema()
          data = json.loads(request.data)

          #Load user login data against schema
          check_user = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","Email","League"))


          #Find user in database with associated username
          results = collection.find_one({"Username": check_user['Username']})


          #Check if no results have been returned
          if not results:
              print ("No user found")
              return

          #Now check password to verify user and login
          if VerifyPassword(check_user['Password'], results['Password']):
              print ("Login Successful")
          else:
              print ("Invalid Password")



class Users(Resource):
    def get(self):

        #Try to load JSON get request
        data = json.loads(request.data)

        #Check for matching username in collection
        results = collection.find_one({"Username": data['Username']})

        #If no results return error
        if not results:
            print("No user found")

        #If passwords dont match return error
        if not VerifyPassword(data['Password'], results['Password']):
            print("Password invalid")

        #Try to delete password and ID keys from dictionary
        try:
            del (results['Password'],results['_id'])
        except KeyError:
            print("Key not found in dictionary")

        #Return user information to client
        return results


api.add_resource(Login, '/Login')
api.add_resource(Register, '/Register')
api.add_resource(Users, '/Users')


if __name__ == '__main__':
    app.run(debug=True)
