import pytest
from unittest.mock import patch, MagicMock
import pytest
import json
from app import routes
from app.dynamodb import create_user_management_tables, add_user
import logging

def test_endpoint(client):
    response = client.get('/fail')
    assert response.status_code == 405

def test_add_shop(client):
    # Setup: Create a table and add an item
    shop_data =  {
        "email": "electro@example.com",
        "password": "password33",
        "shop_name": "Max Electro",
        "description": "Join me on my sustainability journey",
        "address": "Weinhofstrasse 123, Luzern",
        "phone": "3456789012",
    }
    # POST request to '/shops' to register a new shop
    response = client.post('/shops', data=json.dumps(shop_data), content_type='application/json')
    logging.info(response)
    # Check if the request was successful
    assert response.status_code == 200
    response_json = response.get_json()
    assert response.json['status'] == True
    assert 'shop_id' in response_json['value'], "shop_id key is missing in the response"
    assert response_json['value']['address'] == shop_data['address']
    assert response_json['value']['email'] == shop_data['email']
    assert response_json['value']['phone'] == shop_data['phone']
    assert response_json['value']['shop_name'] == shop_data['shop_name']
    assert response_json['value']['type'] == "Shop"
    assert response_json['value']['description'] == shop_data['description']

def test_login_success(client, shop_uuid):
    response = client.post('/login', json={'email': 'newshop@example.com', 'password': 'shopsecure123'})
    assert response.status_code == 200
    assert response.json['status'] == True


def test_login_fail(client, shop_uuid):
    response = client.post('/login', json={'email': 'wrong_mail@example.com', 'password': 'shopsecure123'})
    assert response.status_code == 401
    assert response.json['status'] == False
    assert response.json['message'] == "Invalid login credentials"

def test_update_shop(client, shop_uuid):
    # Setup: Update data for shop
    update_data = {
        "action": "update",
        "shop_name": "Update",
        "description": "Update description",
        "email": "newshop@example.com",
        "address": "456 New St, Newville",
        "profile_picture": "",
        "shop_pictures": [],
        "phone": "0987654321",
    }
    # PUT request to '/shops/<shop_uuid>' to update a shop
    response = client.put(f'/shops/{shop_uuid}', data=json.dumps(update_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['status'] == True
    assert response_json['value']['shop_id'] == shop_uuid
    assert response_json['value']['address'] == update_data['address']
    assert response_json['value']['email'] == update_data['email']
    assert response_json['value']['phone'] == update_data['phone']
    assert response_json['value']['shop_name'] == update_data['shop_name']
    assert response_json['value']['type'] == "Shop"
    assert response_json['value']['description'] == update_data['description']


def test_get_shop_success(client, shop_uuid):
    expected_response = {
        "shop_id": shop_uuid,
        "type": "Shop",
        "email": "newshop@example.com",
        "shop_name": "New Shop",
        "description": "A new shop specializing in eco-friendly products",
        "address": "456 New St, Newville",
        "phone": "0987654321",
        "profile_picture": "",
        "shop_pictures": [],
    }
    response = client.get(f'/shops/{shop_uuid}')
    assert response.status_code == 201
    assert response.get_json()['status'] == True
    assert response.get_json()['value'] == expected_response


def test_get_shop_failure(client):
    shop_uuid = "fas89fasf8898afs89df"
    response = client.get(f'/shops/{shop_uuid}')
    assert response.status_code == 400
    assert response.get_json()['status'] == False
    assert response.get_json()['message'] == "No entity or failed to retrieve it"


def test_delete_shop_success(client, shop_uuid):
    response = client.delete(f'/shops/{shop_uuid}')
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['value'] == "Deleted successfully"
