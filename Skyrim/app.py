from flask import Flask, request
from flask_restplus import Api, Resource
from passlib.hash import sha256_crypt
import pprint
import json
import re
import pymongo
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from paapi import PaApi
from paschema import UserSchema
from pamongo import Authorization,\
                    collection,\
                    authCollection

from pacrypto import EncryptPassword,\
                     VerifyPassword,\
                     GenerateToken


app = Flask(__name__)
api = Api(app)


apiClient = PaApi


class Register(Resource):
    def post(self):

        #Load schema
        schema = UserSchema()

        #Try to load json data
        try:
            data=json.loads(request.data)
        except Exception as e:
            return apiClient.badRequest("Invalid json")

        #Create new user by loading data from dictionary into UserSchema
        new_user = schema.load(data)

        #Now validate formatting of user data with validate_Data method
        UserSchema.validate_Data(new_user)

        #Check to see if username is taken
        if collection.find_one({"Username": new_user['Username']}):
            return apiClient.badRequest("Username already in use")

        #Check if user exists in DB
        if collection.find_one({"Email": new_user['Email']}):
            return apiClient.badRequest("You already have an account")
        else:
            #Create timestamp and update new_user data for db entry
            ts = datetime.utcnow().isoformat
            new_user.update(Timestamp = ts)
            collection.insert_one(new_user)
            return apiClient.success("User added")


class Login(Resource):
    def post(self):

        #Load schema
        schema = UserSchema()

        try:
            data = json.loads(request.data)
        except Exception as e:
            return apiClient.badRequest("Invalid json")

        #Load user login data against schema
        check_user = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","Email","League"))


        #Find user in database with associated username
        results = collection.find_one({"Username": check_user['Username']})


        #Check if no results have been returned
        if not results:
            return apiClient.notFound("User not found")

        #Now check password to verify user and login
        if not VerifyPassword(check_user['Password'], results['Password']):
            return apiClient.badRequest("Invalid password")

        #Pass generated token to variable
        token = GenerateToken(20)

        #Create insert data dictionary
        insertData = {}
        insertData['Username'] = check_user['Username']
        insertData['Token'] = token

        #Inserting data into authCollection
        authCollection.insert_one(insertData)
        return token

        return apiClient.success("Login successful")


class Users(Resource):
    def get(self):

        try:
            data = json.loads(request.data)
        except Exception as e:
            return apiClient.badRequest("Invalid json")

        #TODO load into schema and return 404 if not found
        if "Token" not in data:
            return "Token not found"

        #Pass token to variable
        token = data['Token']

        #Use method to get associated username from given token
        username = Authorization(token)

        #If no token found return error 401
        if not username:
            return apiClient.unAuthorized("User not authorized")

        #Check for matching username in collection
        results = collection.find_one({"Username": username})

        #If no results return error
        if not results:
            return apiClient.notFound("User not found")

        #Try to delete password and ID keys from dictionary
        try:
            del (results['Password'],results['_id'])
        except KeyError:
            return apiClient.internalServerError()

        return results



api.add_resource(Login, '/Login')
api.add_resource(Register, '/Register')
api.add_resource(Users, '/Users')


if __name__ == '__main__':
    app.run(debug=True)
