import pytest
from unittest.mock import patch, MagicMock
import json
from app import routes_reviews

def test_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_review(client):
    # Setup: Create a table and add an item
    review_data = {
        "product_id": "1234",
        "customer_id": "4321", 
        "reviewcontent": "Greate Design.",
        "rating": "5"
    }
    # POST request to '/users' to register a new user
    response = client.post('/review', data=json.dumps(review_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    assert response.json['status'] == True
    assert response.json['value'] == "Successfully added Review"

def test_edit_review(client):
    review_data = {
        "product_id": "1234",
        "customer_id": "4321", 
        "reviewcontent": "Greate Design.",
        "rating": "5"
    }
    # POST request to '/users' to register a new user
    #client.post('/review', data=json.dumps(review_data), content_type='application/json')
    response = client.get('/review/1234')
    assert response.status_code == 200
    assert response.json['status'] == False
    #response_value = response.json['value'][0]
    #assert response_value['review_id'] != ""
    #review_id = response_value['review_id']

    #review_newdata = {
    #    "product_id": "1234",
    #    "customer_id": "4321", 
    #    "reviewcontent": "Good Design.",
    #    "rating": "4",
    #    "review_id": review_id
    #}
    
    #response = client.put('/users', data=json.dumps(review_newdata), content_type='application/json')
    #response_get = client.get('/review/1234')
    #assert response_get.status_code == 200
    #response_getjs = response_get.json['value']
    #response_value = response_getjs[0]
    #assert response_value['review_id'] == review_id
    #assert response_value['product_id'] == review_newdata['product_id']
    #assert response_value['customer_id'] == review_newdata['customer_id']
    #assert response_value['reviewcontent'] == review_newdata['reviewcontent']
    #assert response_value['rating'] == review_newdata['rating']

#def test_delete_review(client):
#    assert None

