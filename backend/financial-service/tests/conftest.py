import pytest
from app import routes, create_app
import json
from app.dynamodb import create_accounts_table, delete_accounts_table


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
    create_accounts_table()

def teardown_dynamodb():
    # Delete table after testing
    delete_accounts_table()


@pytest.fixture
def account_uuid(client):
    # Data for a new account
    shop_data = {
        "shop_id": "af7asf698g76adf6s7fdf7a8fasd0f",
    }
    # Create a new account
    response = client.post('/account', data=json.dumps(shop_data), content_type='application/json')
    # Assume the POST endpoint returns a JSON with the shop's UUID
    account_uuid = response.get_json()['value']
    return account_uuid