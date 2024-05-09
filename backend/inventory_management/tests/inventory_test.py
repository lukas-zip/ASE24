from unittest.mock import patch, MagicMock
import pytest
import json
from app import routes
from app.dynamodb import create_product_table, add_product

def test_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200


