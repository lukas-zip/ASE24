from app import dynamodb
import json

def add_dummy_data():
    with open('dummydata/users.json', 'r') as f:
        dummy_users = json.load(f)
    for user in dummy_users:
        dynamodb.add_user(email=user["email"], password=user["password"], username=user["username"], address=user["address"],
                          phone=user["phone"], profile_picture=user["profile_picture"], dummyid=user["dummyid"])


    with open('dummydata/shops.json', 'r') as f:
        dummy_shops = json.load(f)
    for shop in dummy_shops:
        dynamodb.add_shop(shop_name=shop["shop_name"], description=shop["description"], email=shop["email"], password=shop["password"],
                          address=shop["address"], phone=shop["phone"], profile_picture=shop["profile_picture"], shop_pictures=shop["shop_pictures"], dummyid=shop["dummyid"])