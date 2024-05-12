import json
from unittest.mock import patch


def test_endpoint(client):
    response = client.get("/")
    assert response.status_code == 201


def test_get_all_orders(client):
    response = client.get("/orders")
    response_data = json.loads(response.data)
    response_data["value"]["Count"] = 0


def test_add_order(client):
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["value"]["user_id"] == order_data["user_id"]
    # check only one product is available in order
    assert len(response_json["value"]["orders_fe"]) == 1
    assert (
        response_json["value"]["orders_fe"][0]["product_id"] == order_data["product_id"]
    )
    assert response_json["value"]["orders_fe"][0]["quantity"] == order_data["quantity"]
    assert response_json["value"]["order_status"] == "unpaid"
    expected_total_price = 100.0 * float(order_data["quantity"])
    assert float(response_json["value"]["total_price"]) == expected_total_price


def test_get_order_by_id(client):

    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    response_json = response.get_json()
    order_id = response_json["value"]["order_id"]

    # update order
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200


def test_delete_order_by_id(client):
    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    response_json = response.get_json()
    order_id = response_json["value"]["order_id"]

    # update order
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200


def test_update_order(client):

    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    response_json = response.get_json()
    order_id = response_json["value"]["order_id"]

    update_order_data = {
        "product_id": "product_id_test1",
        "quantity": 2,
    }
    response = client.put(
        f"/orders/{order_id}",
        data=json.dumps(update_order_data),
        content_type="application/json",
    )
    response_json = response.get_json()

    assert response.status_code == 200
    # check price is calculated correctly
    expected_total_price = 100.0 * float(order_data["quantity"]) + 90.0 * float(
        update_order_data["quantity"]
    )
    assert float(response_json["value"]["total_price"]) == expected_total_price
    assert response_json["value"]["order_status"] == "unpaid"


def test_set_order_to_paid(client):
    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    response_json = response.get_json()
    order_id = response_json["value"]["order_id"]

    # change status to paid
    response = client.get(f"/orders/{order_id}/status/paid")
    response_json = response.get_json()
    assert response.status_code == 200

    assert response_json["value"]["order_status"] == "paid"


def test_search_unpaid_orders(client):
    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    assert response.status_code == 200

    # search unpaid user orders
    response = client.get("/orders/search/status/unpaid")

    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json["value"]["Count"] == 1
    assert response_json["value"]["Items"][0]["order_status"] == "unpaid"


def test_search_paid_orders(client):
    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    response_json = response.get_json()
    order_id = response_json["value"]["order_id"]
    assert response.status_code == 200

    # change status to paid
    response = client.get(f"/orders/{order_id}/status/paid")
    response_json = response.get_json()
    assert response.status_code == 200

    # search paid user orders
    response = client.get("/orders/search/status/paid")
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json["value"]["Count"] == 1
    assert response_json["value"]["Items"][0]["order_status"] == "paid"


def test_search_po_unpaid_orders(client):
    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    assert response.status_code == 200

    # search unpaid po orders
    response = client.get("/orders/product/search/status/unpaid")
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json["value"]["Count"] == 1
    assert response_json["value"]["Items"][0]["order_status"] == "unpaid"


def test_set_po_order_to_paid(client):
    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    response_json = response.get_json()
    order_id = response_json["value"]["order_id"]

    # change po order status to paid
    response = client.get(
        f"/orders/product/{order_id}/{'1324a686-c8b1-4c84-bbd6-17325209d78c6'}/paid"
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json["value"]["order_status"] == "paid"


def test_search_po_order_by_paid_status(client):
    # Add order
    order_data = {
        "user_id": "username_test",
        "product_id": "product_id_test0",
        "quantity": 7,
    }
    response = client.post(
        "/orders", data=json.dumps(order_data), content_type="application/json"
    )
    response_json = response.get_json()
    order_id = response_json["value"]["order_id"]

    # change po order status to paid
    response = client.get(
        f"/orders/product/{order_id}/{'1324a686-c8b1-4c84-bbd6-17325209d78c6'}/paid"
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json["value"]["order_status"] == "paid"

    # search paid po orders
    response = client.get("/orders/product/search/status/paid")
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json["value"]["Count"] == 1
    assert response_json["value"]["Items"][0]["order_status"] == "paid"
