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