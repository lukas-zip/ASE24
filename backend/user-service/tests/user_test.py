import pytest
from unittest.mock import patch, MagicMock
import pytest
import json
from app import routes
from app.dynamodb import create_user_management_tables, add_user
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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

def test_login_success(client, user_uuid):
    response = client.post('/login', json={'email': 'testuser@example.com', 'password': 'testpass123'})
    assert response.status_code == 200
    assert response.json['status'] == True


def test_login_fail(client, user_uuid):
    response = client.post('/login', json={'email': 'testuser@example.com', 'password': 'false_password'})
    assert response.status_code == 401
    assert response.json['status'] == False
    assert response.json['message'] == "Invalid login credentials"

def test_update_user(client, user_uuid):
    # Setup: Update data for user
    update_data = {
        "action": "update",
        "email": "update@example.com",
        "password": "testpass123",
        "username": "update",
        "address": "123 Test St, Testville",
        "phone": "1234567890",
        "profile_picture": "",
    }
    # PUT request to '/users/<user_uuid>' to update a user
    response = client.put(f'/users/{user_uuid}', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['status'] == True
    assert response_json['value']['user_id'] == user_uuid
    assert response_json['value']['address'] == update_data['address']
    assert response_json['value']['email'] == update_data['email']
    assert response_json['value']['phone'] == update_data['phone']
    assert response_json['value']['profile_picture'] == ""
    assert response_json['value']['type'] == "User"
    assert response_json['value']['username'] == update_data['username']

def test_change_password(client, user_uuid):
    # Setup: Password change data
    update_data = {
        "action": "password",
        "old_password": "testpass123",
        "new_password": "newPassword123",
    }
    # PUT request to '/users/<entity_uuid>' for password change
    response = client.put(f'/users/{user_uuid}', data=json.dumps(update_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['status'] == True

def test_get_user_success(client, user_uuid):
    # Expected mock response from your database or service
    expected_response = {
        "user_id": user_uuid,
        "type": "User",
        "email": "testuser@example.com",
        "username": "test",
        "address": "123 Test St, Testville",
        "phone": "1234567890",
        "profile_picture": "",
    }
    response = client.get(f'/users/{user_uuid}')
    assert response.status_code == 201
    assert response.get_json()['status'] == True
    assert response.get_json()['value'] == expected_response


def test_get_user_failure(client):
    # Expected mock response from your database or service
    user_uuid = "asf92349090390wfasf"
    response = client.get(f'/users/{user_uuid}')
    assert response.status_code == 400
    assert response.get_json()['status'] == False
    assert response.get_json()['message'] == "No entity or failed to retrieve it"


def test_delete_user_success(client, user_uuid):
    # Mock the DynamoDB and S3 interactions
    response = client.delete(f'/users/{user_uuid}')
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['value'] == "Deleted successfully"
