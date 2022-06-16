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
        ratingId = req.route_params['ratingId']
    except Exception:
        return func.HttpResponse(f"No ratingId provides in route", status_code=400)
    
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

    for r in ratings:
        if r['id'] == ratingId:
            return func.HttpResponse(json.dumps(r), status_code=200)
    return func.HttpResponse(f"No rating with id: {ratingId}", status_code=400)
