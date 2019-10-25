from flask import Flask, request
from flask_restplus import Api, Resource
from passlib.hash import sha256_crypt
import pprint
import json
import re
import pymongo
from marshmallow import ValidationError
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

apiClient = PaApi()


class Register(Resource):
    def post(self):

        #Load schema
        schema = UserSchema()

        #Try to load json data
        try:
            data=json.loads(request.data)
        except Exception as e:
            return "Invalid json", 400

        #Create new user by loading data from dictionary into UserSchema
        try:
            new_user = schema.load(data, partial=("Token",))
        except ValidationError as err:
            return err.messages, 400

        #Now validate formatting of user data with validate_Data method
        try:
            UserSchema.validate_Data(new_user)
        except ValidationError as err:
            return err.messages, 400

        #Check to see if username is taken
        if collection.find_one({"Username": new_user['Username']}):
            return "Username already in use", 400

        #Check if user exists in DB
        if collection.find_one({"Email": new_user['Email']}):
            return "You already have an account", 400
        else:
            #Create timestamp and update new_user data for db entry
            ts = datetime.utcnow().isoformat()
            new_user.update(Timestamp = ts)
            collection.insert_one(new_user)
            return "User added", 200

        #TODO email verification


class Login(Resource):
    def post(self):

        #Load schema
        schema = UserSchema()

        try:
            data = json.loads(request.data)
        except Exception as e:
            return "Invalid json", 400

        #Load user login data against schema
        try:
            check_user = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","Email","League","Token",))
        except ValidationError as err:
            return err.messages, 400

        #Find user in database with associated username
        results = collection.find_one({"Username": check_user['Username']})


        #Check if no results have been returned
        if not results:
            return "User not found", 404

        #Now check password to verify user and login
        if not VerifyPassword(check_user['Password'], results['Password']):
            return "Invalid password", 400

        #Pass generated token to variable
        token = GenerateToken(20)

        #Create insert data dictionary
        insertData = {}
        insertData['Username'] = check_user['Username']
        insertData['Token'] = token

        #Inserting data into authCollection
        authCollection.insert_one(insertData)
        return token



class Users(Resource):
    def get(self):

        schema = UserSchema()

        try:
            data = json.loads(request.data)
        except Exception as e:
            return "Invalid json", 400

        #Load into schema and return 404 if not found
        try:
            auth = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","Email","League","Username","Password",))
        except ValidationError as err:
            return err.messages, 404

        #Pass token to variable
        token = auth['Token']

        #Use method to get associated username from given token
        username = Authorization(token)

        #If no token found return error 401
        if not username:
            return apiClient.unAuthorized()

        #Check for matching username in collection
        results = collection.find_one({"Username": username})

        #If no results return error
        if not results:
            return "User not found", 404

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
