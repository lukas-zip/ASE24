from app import dynamodb_users
import json

def add_dummy_data():
    with open('dummydata/orders.json', 'r') as f:
        dummy_orders = json.load(f)
    for order in dummy_orders:
        dynamodb_users.add_order(user_id=order["user_id"], orders='', total_price=order["total_price"], execution_time=order["execution_time"], order_status=order["order_status"])

