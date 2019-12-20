import json, requests
from flask import Response



class PaApi(object):
    
    #200
    def success(self, headers, text):
        #set status code 200
        response = Response()
        response.status_code = 200
        response.data = text
        return response

    #400
    def badRequest(self, text):
        #set status code 400
        response = Response()
        response.status_code = 400
        response.data = text
        return response

    #401
    def unAuthorized(self):
        #set status code
        response = Response()
        response.status_code = 401
        return response

    #403
    def forbidden(self):
        #set status code
        response = Response()
        response.status_code = 403
        return response

    #404
    def notFound(self, text):
        #set status code
        response = Response()
        response.status_code = 404
        response.data = text
        return response

    #500
    def internalServerError(self):
        #set status code 500
        response = Response()
        response.status_code = 500
        return response

    def returnHtml(self, html):
        response = Response()
        response.status_code = 504
        response.data = html
        return response
        
    
