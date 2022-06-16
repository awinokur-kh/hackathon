from datetime import datetime
import logging
import uuid
import azure.functions as func
from datetime import datetime
import requests
import json

def main(req: func.HttpRequest, doc: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    ratings = [
        {
            "id": rating['id'],
            "timestamp": rating['timestamp'],
            "userid": rating['userid'],
            "productId": rating['productId'],
            "locationName":rating['locationName'],
            "rating":rating['rating'],
            "userNotes":rating['userNotes']
        }
        for rating in doc
    ]

    return func.HttpResponse(json.dumps(ratings), status_code=200)
