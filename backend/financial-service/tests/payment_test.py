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

