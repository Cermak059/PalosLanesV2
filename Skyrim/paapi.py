import json, requests
from flask import Response



class PaApi(object):
    def __init__(self, mongoClient, logger):
        self.mongoClient = mongoClient
        self.logger = logger

    #200
    def success(self):
        #set status code 200
        response = Response()
        response.status_code = 200
        return response

    #400
    def badRequest(self):
        #set status code 400
        response = Response()
        response.status_code = 400
        return response

    #401
    def unAuthorized(self):
        #set status code
        response = Response()
        response.status_code = 401
        return response

    #404
    def notFound(self):
        #set status code
        response = Response()
        response.status_code = 404
        return response

    #500
    def internalServerError(self):
        #set status code 500
        response = Response()
        response.status_code = 500
        return response
    
