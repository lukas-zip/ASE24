from app import dynamodb
import json

def add_dummy_data():
    with open('dummydata/users.json', 'r') as f:
        dummy_users = json.load(f)
    for user in dummy_users:
        dynamodb.add_user(email=user["email"], password=user["password"], username=user["username"], address=user["address"],
                          phone=user["phone"])


    with open('dummydata/shops.json', 'r') as f:
        dummy_shops = json.load(f)
    for shop in dummy_shops:
        dynamodb.add_shop(shop_name=shop["shop_name"], description=shop["description"], email=shop["email"], password=shop["password"],
                          address=shop["address"], phone=shop["phone"])