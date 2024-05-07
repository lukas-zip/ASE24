import pytest
from app import routes, create_app
import json
from app.dynamodb import get_dynamodb_resource, create_user_management_tables, delete_user_management_tables


@pytest.fixture()
def client():
    test_app = create_app()
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        with test_app.app_context():
            setup_dynamodb()  # Setup your DynamoDB tables here
        yield client
        teardown_dynamodb()

def setup_dynamodb():
    # Create table for testing
    create_user_management_tables()


def teardown_dynamodb():
    # Delete table after testing
    delete_user_management_tables()


@pytest.fixture
def user_uuid(client):
    # Data for a new user
    user_data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "username": "test",
        "address": "123 Test St, Testville",
        "phone": "1234567890",
    }
    # Create a new user
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    # Assume the POST endpoint returns a JSON with the user's UUID
    user_uuid = response.get_json()['value']['user_id']
    return user_uuid

@pytest.fixture
def shop_uuid(client):
    # Data for a new shop
    shop_data = {
        "email": "newshop@example.com",
        "password": "shopsecure123",
        "shop_name": "New Shop",
        "description": "A new shop specializing in eco-friendly products",
        "address": "456 New St, Newville",
        "phone": "0987654321",
    }
    # Create a new shop
    response = client.post('/shops', data=json.dumps(shop_data), content_type='application/json')
    # Assume the POST endpoint returns a JSON with the shop's UUID
    shop_uuid = response.get_json()['value']['shop_id']
    return shop_uuid