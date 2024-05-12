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


@pytest.fixture(autouse=True)
def mock_get_product_details():
    with patch("app.utils.get_product_details") as mock:
        # Define the behavior of the mock function
        def get_product_details_mock(product_id):
            if product_id == "product_id1":
                product_price = 100.0
                product_price_reduction = 10.0
                product_owner = "po1"
            elif product_id == "product_id2":
                product_price = 50.0
                product_price_reduction = 5.0
                product_owner = "po1"
            elif product_id == "product_id3":
                product_price = 500.0
                product_price_reduction = 50.0
                product_owner = "po2"
            elif product_id == "product_id4":
                product_price = 1000.0
                product_price_reduction = 5.0
                product_owner = "po2"
            else:
                product_price = None
                product_price_reduction = None
                product_owner = None
            return product_price, product_price_reduction, product_owner

        # Assign the mock function to the patched function
        mock.side_effect = mock_get_product_details

        yield mock


@pytest.fixture()
def mock_get_all_product_details():
    with patch("app.utils.mock_get_all_product_details") as mock:
        # Define the behavior of the mock function
        def get_product_details_mock():
            res = {
                "product_assemblies": "Final",
                "product_bom": ["UUID1"],
                "product_category": ["Necless"],
                "product_current_stock": "10",
                "product_description": "Description of Product Y",
                "product_id": "61363bc2-0aba-4d0f-aa84-4e4af17086b6",
                "product_name": "Product Y",
                "product_owner": "1324a686-c8b1-4c84-bbd6-17325209d78c6",
                "product_picture": [
                    "http://localhost:4566/productpictures/thisexampleproduct.png"
                ],
                "product_price": "100",
                "product_price_reduction": "10",
                "product_reviews": [""],
                "product_sale": False,
                "product_search_attributes": ["Greenish", "Platin"],
                "product_should_stock": "20",
            }
            return res

        # Assign the mock function to the patched function
        mock.side_effect = mock_get_all_product_details

        yield mock
