import pytest
from app import routes, create_app
from app.dynamodb import create_product_table, delete_product_table, create_product_owner_index, create_gsi #get_dynamodb_resource, create_user_management_tables, delete_user_management_tables
from app.s3 import create_bucket

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
    create_product_table()
    create_product_owner_index()
    create_bucket()
    #create_gsi()

def teardown_dynamodb():
    # Delete table after testing
    delete_product_table()