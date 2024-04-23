import pytest
from unittest.mock import patch, MagicMock
import pytest
import json
from app import routes
from app.dynamodb import create_user_management_tables, add_user


def test_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add_user(client):
    # Setup: Create a table and add an item
    user_data = {
        "email": "jane.doe@example.com",
        "password": "password2",
        "username": "janedoe",
        "address": "Jane Road, Bern 23456",
        "phone": "2345678901"
    }
    # POST request to '/users' to register a new user
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    response_json = response.get_json()
    assert response.json['status'] == True
    assert 'user_id' in response_json['value'], "user_id key is missing in the response"
    assert response_json['value']['address'] == user_data['address']
    assert response_json['value']['email'] == user_data['email']
    assert response_json['value']['phone'] == user_data['phone']
    assert response_json['value']['profile_picture'] == ""
    assert response_json['value']['type'] == "User"
    assert response_json['value']['username'] == user_data['username']


def test_login(client):
    # Setup: Create a table and add an item
    user_data = {
        "email": "jane.doe@example.com",
        "password": "password2",
        "username": "janedoe",
        "address": "Jane Road, Bern 23456",
        "phone": "2345678901"
    }
    # POST request to '/users' to register a new user
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    response_json = response.get_json()
    assert response.json['status'] == True
    assert 'user_id' in response_json['value'], "user_id key is missing in the response"
    assert response_json['value']['address'] == user_data['address']
    assert response_json['value']['email'] == user_data['email']
    assert response_json['value']['phone'] == user_data['phone']
    assert response_json['value']['profile_picture'] == ""
    assert response_json['value']['type'] == "User"
    assert response_json['value']['username'] == user_data['username']


def test_login_success(client):
    user_data = {
        "email": "jane.doe@example.com",
        "password": "password2",
        "username": "janedoe",
        "address": "Jane Road, Bern 23456",
        "phone": "2345678901"
    }
    client.post('/users', data=json.dumps(user_data), content_type='application/json')
    response = client.post('/login', json={'email': 'jane.doe@example.com', 'password': 'password2'})
    assert response.status_code == 200