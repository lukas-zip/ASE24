from unittest.mock import patch, MagicMock
import pytest
import json
from app import routes
from app.dynamodb import create_product_table, add_product
import os

products_ids = []

def test_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200

def testing_dummy_data(client):
    #loading dummy_data
    with open('dummydata/products.json', 'r') as f:
        dummy_products = json.load(f)

    response = client.get('/productsbyowner')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    supposed_products = response_data['value']
    for i in supposed_products:
        products_ids.append(i['product_id'])
    assert response_data['status'] == True
    assert 'value' in response_data
    assert len(response_data) == len(dummy_products)


def test_add_product(client):

    product_data = {
        "product_owner": "1324a686-c8b1-4c84-bbd6-17325209d78c6",
        "product_name": "TestingProduct",
        "product_description": "Description of Product Y",
        "product_current_stock": 10,
        "product_should_stock": 20,
        "product_price": 50.00,
        "product_picture": ["http://localhost:4566/productpictures/thisexampleproduct.png"],
        "product_price_reduction": 0.00,
        "product_sale": False,
        "product_category": ["something"],
        "product_search_attributes": ["Black", "Cropped"],
        "product_reviews": ["Review1"],
        "product_bom": ["1234567890", "0987654321"],
        "product_assemblies": "Final"
    }

    response = client.post('/product/insert', data = json.dumps(product_data), content_type='application/json')

    assert response.status_code == 200
    response_json = response.get_json()
    assert response.json['status'] == True
    assert response.json['value'] == "Product inserted successfully."

# testing missing required fields.
def test_insert_product_missing_required_fields(client):
    # Define test data with missing required fields
    data = {
        
    }

    # Send POST request with test data
    response = client.post('/product/insert', json=data, content_type='application/json')

    # Check response status code
    assert response.status_code == 400

    # Check response data
    data = json.loads(response.data)
    assert data['status'] == False
    assert 'error' in data

def test_insert_product_with_negative_stock(client):
    # Define test data
    data = {
        "product_owner": "John Doe",
        "product_name": "Test Product",
        "product_description": "This is a test product.",
        "product_current_stock": -10,
        "product_should_stock": 20,
        "product_price": 99.99,
        "product_picture": [],
        "product_price_reduction": 0.00,
        "product_sale": False,
        "product_category": [],
        "product_search_attributes": [],
        "product_reviews": [],
        "product_bom": [],
        "product_assemblies": ""
    }

    #data_json = json.dumps(data)

    # Send POST request with test data
    response = client.post('/product/insert', json=data, content_type='application/json')

    # Check response status code
    assert response.status_code == 400

    # Check response data
    data = json.loads(response.data)
    assert data['status'] == False
    assert 'error' in data

def test_get_product(client):

    for product_id in products_ids:
        response = client.get('/product/{product_id}')
        assert response.status_code == 200  # Assuming 200 for success



# def test_upload_picture(client):
#     # Define test files
#     file_path = '/Users/felix/Desktop/projectASE/ASE24/backend/inventory_management/tests/testing_data_pictures/Model-of-Architecture-of-an-Ecosystem-The-Architecture-of-an-Ecosystem-deals-with-the.png'
#     file = {
#         'image': ('Model-of-Architecture-of-an-Ecosystem-The-Architecture-of-an-Ecosystem-deals-with-the.png', open(file_path, 'rb'), 'application/png'),
#         # Add more test files here
#     }

#     # Send POST request with test files
#     response = client.post('/product/upload/picture', files=file)

#     # Check response status code
#     assert response.status_code == 200

#     # Check response data
#     data = response.json()
#     assert data['status'] == True
#     assert 'value' in data
#     assert 'http://localhost:4566/productpictures/' in data['value']
