import pytest
#from app import create_app
from app import create_app
from app.dynamodb_reviews import create_review_tables, delete_review_tables

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
    create_review_tables()


def teardown_dynamodb():
    # Delete table after testing
    delete_review_tables()