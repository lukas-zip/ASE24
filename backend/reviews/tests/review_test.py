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
    # POST request to '/review' to register a new review
    response = client.post('/review', data=json.dumps(review_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    assert response.json['status'] == True
    assert response.json['value'] == "Successfully added Review"

    review2_data = {
        "customer_id": "4321", 
        "reviewcontent": "Greate Design.",
        "rating": "5"
    }
    # POST request to '/review' to register a new review
    response = client.post('/review', data=json.dumps(review2_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 400
    assert response.json['status'] == False
    assert response.json['message'] == "Product_ID, Customer_ID and rating are required!"

def test_check_review(client):
    review_data = {
        "product_id": "1234",
        "customer_id": "4321", 
        "reviewcontent": "Greate Design.",
        "rating": "5"
    }
    check_data = {
        "product_id": "1234",
        "customer_id": "4321"        
    }
    # Check the extistance of a review for that user and product
    response = client.get('/review/check', data=json.dumps(check_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    assert response.json['status'] == True
    assert response.json['value'] == "Customer has not jet made a review for this product"
    
    # POST request to '/review' to register a new review
    client.post('/review', data=json.dumps(review_data), content_type='application/json')

    # Check the extistance of a review for that user and product
    response = client.get('/review/check', data=json.dumps(check_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    assert response.json['status'] == False
    assert response.json['message'] == "Review already exists"