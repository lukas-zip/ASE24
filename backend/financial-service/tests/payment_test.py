import pytest
import json
from app import routes
import logging
import re

def test_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_account_success(client):
    shop_id = 'asdfag78fd6gfdg56adf57s6f5d7saf'
    response = client.post('/account', data=json.dumps({'shop_id': shop_id}), content_type='application/json')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response.json['status'] == True
    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    assert re.match(uuid_pattern, response_json['value']), "account_id key is missing in the response or is invalid"


def test_account_in_db_success(client, account_uuid):
    shop_uuid = "af7asf698g76adf6s7fdf7a8fasd0f"
    response = client.get(f'/account/{shop_uuid}')
    logging.info(response)
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['value']['account_id'] == f"{account_uuid}"
    assert response.get_json()['value']['shop_id'] == f"{shop_uuid}"
    assert response.get_json()['value']['balance'] == f"0"


def test_account_in_db_failure(client):
    shop_uuid = "xxxxxxxxxx"
    response = client.get(f'/account/{shop_uuid}')
    assert response.status_code == 400
    assert response.get_json()['status'] == False
    assert response.get_json()['message'] == "Unable to retrieve account."


