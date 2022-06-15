from datetime import datetime
import logging
import uuid
import azure.functions as func
from datetime import datetime
import requests
import json

PRODUCT_ENDPOINT = 'https://serverlessohapi.azurewebsites.net/api/GetProducts'
USER_ENDPOINT = 'https://serverlessohapi.azurewebsites.net/api/GetUsers'

def user_exists(user_id):
    res = requests.get(url=USER_ENDPOINT,params={"userId":user_id})
    return res.status_code == 200

def product_exists(product_id):
    res  = requests.get(url=PRODUCT_ENDPOINT, params={"productId":product_id})
    return res.status_code == 200

def valid_rating(rating):
    return isinstance(rating, int) and rating < 6 and rating > -1

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass

    try:
        userId = req_body.get('userId')
        productId = req_body.get('productId')
        locationName = req_body.get('locationName')
        rating = req_body.get('rating')
        userNotes = req_body.get('userNotes')
    except Exception as ex:
        return func.HttpResponse(
             f"Bad input data: {ex}",
             status_code=400
        )

    if user_exists(userId) and product_exists(productId) and valid_rating(rating):
        newdocs = func.DocumentList() 
        new_rating_id = str(uuid.uuid4())
        newproduct_dict = {
            "id": new_rating_id,
            "timestamp": datetime.now().strftime('%Y%m%d-%H:%M:%S'),
            "userid": userId,
            "productId": productId,
            "locationName":locationName,
            "rating":rating,
            "userNotes":userNotes
        }
        newdocs.append(func.Document.from_dict(newproduct_dict))
        doc.set(newdocs)
        
        return func.HttpResponse(json.dumps(newproduct_dict), status_code=200)
    else:
        return func.HttpResponse(f"User/product/rating Id is invalid. userId:{userId} productId{productId} rating:{rating}", status_code=400)
