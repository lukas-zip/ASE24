from unittest.mock import patch

import pytest
from app import create_app, dynamodb_po, dynamodb_users
from app.utils import get_all_product_details, get_product_details


@pytest.fixture()
def client():
    test_app = create_app()
    test_app.config["TESTING"] = True
    with test_app.test_client() as client:
        with test_app.app_context():
            setup_dynamodb()  # Setup your DynamoDB tables here
        yield client
        teardown_dynamodb()


def setup_dynamodb():
    # Create table for testing
    dynamodb_users.create_orders_table()
    dynamodb_po.create_product_owner_orders_table()


def teardown_dynamodb():
    # Delete table after testing
    dynamodb_users.delete_order_management_tables()
    dynamodb_po.delete_po_order_management_tables()