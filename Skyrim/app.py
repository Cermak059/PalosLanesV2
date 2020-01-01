from flask import Flask, request
from flask_restplus import Api, Resource
from passlib.hash import sha256_crypt
import time
import pprint
import json
import re
import pymongo
import threading
from marshmallow import ValidationError
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from palogger import PaLogger
from pautils import SendEmail
from paapi import PaApi
from paschema import UserSchema
from paconfig import VERIFY_EMAIL_TEMPLATE,\
                     SUCCESS_TEMPLATE,\
                     FORGOT_TEMPLATE,\
                     RESET_TEMPLATE,\
                     CRON_SLEEP_SECONDS,\
                     ADMIN_USERS
from pamongo import Authorization,\
                    resetAuth,\
                    collection,\
                    authCollection,\
                    tempCollection,\
                    pendingReset
from pacrypto import EncryptPassword,\
                     VerifyPassword,\
                     GenerateToken,\
                     getExpirationTime,\
                     TimestampExpired

                
app = Flask(__name__)
api = Api(app)

apiClient = PaApi()
logger = PaLogger()
        
def _removeExpiredPendingUsers():

    #Get current timestamp
    ts = datetime.utcnow().isoformat()

    #Find any expired pending users in tempCollection
    results = tempCollection.find({"Expires": {"$lt":ts}})

    #Now delete any docs found
    for doc in results:
        if tempCollection.delete_one({"_id": doc['_id']}) != 200:
            logger.info("Failed to cleanup expired tokens")
        else:
            logger.info("Cleaned up pending user{}".format(doc['Email']))
    logger.info("Finished cleaning up pending users") 

def _removeExpiredAuthTokens():

    #Get current timestamp
    ts = datetime.utcnow().isoformat()

    #Find any expired auth tokens in authCollection
    results = authCollection.find({"Expires": {"$lt":ts}})

    #Now delete any docs found
    for doc in results:
        if authCollection.delete_one({"_id": doc['_id']}) != 200:
            logger.error("Failed to cleanup expired tokens")
        else:
            logger.info("Cleaned up token{}".format(doc['Token']))
    logger.info("Finished cleaning up expired auth tokens")

def _startCrons():
    ''' Background workers to cleanup expired tokens in db '''
    logger.info("Starting background cron workser")
    t = threading.Thread(target=_scheduler, args=())
    t.start()

def _scheduler():
    while(True):
        logger.info("Running cleanup scripts")
        _removeExpiredAuthTokens()
        _removeExpiredPendingUsers()
        logger.info("Sleeping for {} seconds before running cleanup again".format(CRON_SLEEP_SECONDS))
        time.sleep(CRON_SLEEP_SECONDS)
   
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
            return apiClient.badRequest("Username already in use")
        
        #Check if user exists in DB
        if collection.find_one({"Email": new_user['Email']}):
            return apiClient.badRequest("You already have an account")
        else:
            if re.search("@{}$".format(ADMIN_USERS), new_user['Email']):
                logger.info("Setting {} as admin".format(new_user['Email']))
                new_user['Type'] = "Admin"
            else:
                new_user['Type'] = "User"
                new_user['Points'] = 0

        #Create timestamp
        ts = datetime.utcnow().isoformat()

        #Create expiration time for entry and update new_user
        exp = getExpirationTime(hours=2)

        #Generate tempToken
        tempToken = GenerateToken(6)
        
        new_user.update(TempToken = tempToken, Timestamp = ts, Expires = exp)

        #Insert new user into temp DB
        if not tempCollection.insert_one(new_user):
            logger.error("Falied to create user {} in temp DB".format(new_user['Email']))
            return apiClient.internalServerError()
            
        #Send email to verify user account
        with open(VERIFY_EMAIL_TEMPLATE, 'r') as stream:
            emailBodyTemplate = stream.read()
        emailBody = emailBodyTemplate.format(fname=new_user['Fname'], verify_url="http://3.15.199.174:5000/VerifyUser/{}".format(tempToken))
        SendEmail(new_user['Email'], "Verification", emailBody)
        
        logger.info("User {} added to temp Db and emailed verification token".format(new_user['Email']))
        return apiClient.success("Please check email for verification code")

class VerifyUser(Resource):
    def get(self, verificationToken=None):

        #Check if token exists
        if not verificationToken:
            return apiClient.forbidden()
        
        #Find user with matching token in temp DB    
        tempUser = tempCollection.find_one({"TempToken": verificationToken})

        #Handle errors for no user found and expired token
        if not tempUser:
            return apiClient.badRequest("Token not recognized")
        elif TimestampExpired(tempUser['Expires']):
            return apiClient.badRequest("Token is expired")
        
        #Delete token from tempUser 
        try:
            del (tempUser['TempToken'], tempUser['Expires'])
        except KeyError:
            logger.error("Failed to delete key TempToken from dic")
            return apiClient.internalServerError()
        
        #Insert verified user into DB
        if not collection.insert_one(tempUser):
            logger.error("Failed to insert reg user {} into users DB".format(tempUser['Email']))
            return apiClient.internalServerError()
        
        #Now delete old temp data from DB
        if not tempCollection.delete_one({"TempToken": verificationToken}):
            logger.error("Failed to delete doc with token")
            return apiClient.internalServerError()
        
        #Return success template
        with open(SUCCESS_TEMPLATE, 'r') as stream:
            successTemplate = stream.read()
            
        successPage = successTemplate

        logger.info("User {} has verified their account".format(tempUser['Email']))
        return apiClient.returnHtml(successPage)
        

class Login(Resource):
    def post(self):

        #Load schema
        schema = UserSchema()

        try:
            data = json.loads(request.data)
        except Exception as e:
            return apiClient.badRequest("Invalid json")
          
        #Load user login data against schema
        try:
            check_user = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","Email","League","Token",))
        except ValidationError as err:
            return err.messages, 400

        #Find user in database with associated username
        results = collection.find_one({"Username": check_user['Username']})

          
        #Check if no results have been returned
        if not results:
            return apiClient.notFound("Username not found")

        #Now check password to verify user and login 
        if not VerifyPassword(check_user['Password'], results['Password']):
            return apiClient.badRequest("Invalid password")
            
        #Pass generated token to variable
        token = GenerateToken(20)

        #Create timestamp for token
        ts = datetime.utcnow().isoformat()

        #Get expiration time for token
        exp = getExpirationTime(hours=24)

        #Create insert data dictionary
        insertData = {}
        insertData['Username'] = check_user['Username']
        insertData['Token'] = token
        insertData['TimeStamp'] = ts
        insertData['Expires'] = exp

        #Inserting data into authCollection
        if not authCollection.insert_one(insertData):
            logger.error("Failed to insert data into Auth DB")
            return apiClient.internalServerError()

        retData = apiClient._prepareBody({"AuthToken": token, "AccessLevel": results['Type']})
        
        return apiClient.success(retData)
        
class Users(Resource):
    def get(self):

         #Check if auth token is in headers
        authToken = request.headers.get("X-Auth-Token")
        if not authToken:
            return apiClient.unAuthorized()
        

        #Use method to get associated username from given token
        username = Authorization(authToken)

        
        #If no token found return error 401
        if not username:
            return apiClient.unAuthorized()
            
        #Check for matching username in collection
        results = collection.find_one({"Username": username})
        
        #If no results return error
        if not results:
            return apiClient.notFound("User not found")
      
        #Try to delete password and ID keys from dictionary
        try:
            del (results['Password'],results['_id'],results['Timestamp'])
        except KeyError:
            logger.error("Failed to delete keys in dic")
            return apiClient.internalServerError()

        return results

class ResetRequest(Resource):
    def post(self):

        schema = UserSchema()

        try:
            data = json.loads(request.data)
        except Exception as e:
            return apiClient.badRequest("Invalid json")

        try:
            authUser = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","Token","League","Username","Password",))
        except ValidationError as err:
            return err.messages, 404

        results = collection.find_one({"Email": authUser['Email']})

        if not results:
            return apiClient.notFound("Email not found")

        tempToken = GenerateToken(6)

        tempData = {"Email":authUser['Email'],
                    "Token":tempToken,
                    "Expire":getExpirationTime(hours=1)}

        if not pendingReset.insert_one(tempData):
            logger.error("Failed to create temp data")
            return apiClient.internalServerError()
                    
        #Send email to reset user password
        with open(FORGOT_TEMPLATE, 'r') as stream:
            emailBodyTemplate = stream.read()
        emailBody = emailBodyTemplate.format(user_email=authUser['Email'],reset_url="http://3.15.199.174:5000/ResetPasswordForm/{}".format(tempToken))
        SendEmail(authUser['Email'], "Reset Account Password", emailBody)

class ResetPasswordForm(Resource):
    def get(self, verificationToken=None):
        
        #Check if token exists
        if not verificationToken:
            return apiClient.forbidden()

        #Return reset password template
        with open(RESET_TEMPLATE, 'r') as stream:
            resetTemplate = stream.read()
        responseBody = resetTemplate.format(token=verificationToken, change_password_url="http://3.15.199.174:5000/ChangePassword")
        return apiClient.returnHtml(responseBody)
        
class ChangePassword(Resource):
    def post(self):

        schema = UserSchema()

        try:
            data = json.loads(request.data)
        except Exception as e:
            return apiClient.badRequest("Invalid json")

        try:
            resetUser = schema.load(data, partial=("Fname","Lname","Birthdate","Phone","League","Username","Email",))
        except ValidationError as err:
            return err.messages, 400

        match = re.search("[a-zA-Z0-9_]", resetUser["Password"])
        if match:
              hashedPassword = EncryptPassword(resetUser["Password"])
              resetUser.update({'Password' : hashedPassword})
        else:
            return apiClient.badRequest("Not a valid password")

        token = resetUser['Token']

        email = resetAuth(token)

        if not email:
            return apiClient.unAuthorized()

        results = collection.find_one({"Email": email})

        if not results:
            return apiClient.notFound("Email not found")

        if not collection.update({"Email": results['Email']}, {"$set":{"Password": hashedPassword}}):
            logger.error("Failed to update user {} with new password".format(results['Email']))
            return apiClient.internalServerError()

        if not pendingReset.delete_one({"Token": token}):
            logger.error("Failed to delete pending reset request")
            
        return apiClient.success("Password has been reset")

class Authenticate(Resource):
    def get(self):

        #Check if auth token is in headers
        authToken = request.headers.get("X-Auth-Token")
        if not authToken:
            return apiClient.unAuthorized()

        #Check if token matches in DB
        results = authCollection.find_one({"Token": authToken})
        logger.info("Auth results: {}".format(results))
        
        #if no token in DB
        if not results:
            return apiClient.unAuthorized()
        
        #Check if token has expired
        if TimestampExpired(results['Expires']):
            logger.info("Auth token expired")
            return apiClient.unAuthorized()
        
        #Find user in users DB
        user = collection.find_one({"Username" : results['Username']})
        
        #If no user found return 401
        if not user:
            return apiClient.unAuthorized()

        return apiClient.success({})
        
        
class Health(Resource):
    def get(self):
         return "Palos Lanes is up and running"

#_scheduler()

api.add_resource(Login, '/Login')
api.add_resource(Register, '/Register')
api.add_resource(Users, '/Users')
api.add_resource(VerifyUser, '/VerifyUser/<verificationToken>')
api.add_resource(Health, '/Health')
api.add_resource(ResetRequest, '/ResetRequest')
api.add_resource(ResetPasswordForm, '/ResetPasswordForm/<verificationToken>')
api.add_resource(ChangePassword, '/ChangePassword')
api.add_resource(Authenticate, '/Authenticate')


if __name__ == '__main__':
    _startCrons()
    app.run(debug=True, host= '0.0.0.0')
    
