import pytest
from app import routes, create_app
from app.dynamodb import get_dynamodb_resource, create_user_management_tables, delete_user_management_tables


@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            setup_dynamodb()  # Setup your DynamoDB tables here
        yield client
        teardown_dynamodb()


def setup_dynamodb():
    # Create table for testing
    create_user_management_tables()


def teardown_dynamodb():
    # Delete table after testing
    delete_user_management_tables()