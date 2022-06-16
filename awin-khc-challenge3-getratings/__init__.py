from datetime import datetime
import logging
import uuid
import azure.functions as func
from datetime import datetime
import requests
import json

def main(req: func.HttpRequest, doc: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        user_id = req.route_params['userId']
    except Exception:
        return func.HttpResponse(f"No userId provides in route", status_code=400)

    ratings = [
        {
            "id": rating['id'],
            "timestamp": rating['timestamp'],
            "userId": rating['userid'],
            "productId": rating['productId'],
            "locationName":rating['locationName'],
            "rating":rating['rating'],
            "userNotes":rating['userNotes']
        }
        for rating in doc
    ]

    user_ratings = [r for r in ratings if r['userId'] == user_id]
    return func.HttpResponse(json.dumps(user_ratings), status_code=200)
