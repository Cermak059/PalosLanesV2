from flask import Flask, request
from flask_restplus import Api, Resource
from passlib.hash import sha256_crypt
import json
import re
import pymongo
from pymongo import MongoClient
from paschema import UserSchema
from pacrypto import EncryptPassword, \
                     VerifyPassword

app = Flask(__name__)
api = Api(app)

#setup initial connection to MongoDB cluster and DB
cluster = MongoClient("mongodb+srv://Cermak059:Pieman1993!@cluster0-nuw5p.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["PalosTest"]
collection = db["Users"]

#Create user dictionary
users = {}


class Register(Resource):
    def post(self):
        #Instantiate schema and load requested data into dictionary
        schema = UserSchema()
        data=json.loads(request.data)
        #Create new user by loading data from dictionary into UserSchema
        new_user = schema.load(data)
        #Uodate the users dictionary with new user after passing schema
        users.update(new_user)
        #Now validate formatting of user data with validate_Data method
        UserSchema.validate_Data(users)
        #Insert user into DB
        collection.insert_one(users)

        print(users)
        return{'result' : 'User added'}, 201

class Login(Resource):
     def post(self):
          #Instantiate schema and load login data into dictionary
          schema = UserSchema()
          data = json.loads(request.data)
          #Check user login data against schema
          check_user = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","Email","League"))
          #Create new variables for password verification
          chck_Password = data['Password']
          stored_Password = users['Password']
          #Determine if stored and password to check match
          #If so log in
          if VerifyPassword(chck_Password, stored_Password):
              print ("Login Successful")
          else:
              print ("Login Failed")



api.add_resource(Login, '/Login')
api.add_resource(Register, '/Register')


if __name__ == '__main__':
    app.run(debug=True)
