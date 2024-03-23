from app import dynamodb

# Function to add dummy users
def add_dummy_data():
    dummy_users = [
        {"email": "john.doe@example.com", "password": "password1", "username": "johndoe"},
        {"email": "jane.doe@example.com", "password": "password2", "username": "janedoe"},
        {"email": "max.smith@example.com", "password": "password3", "username": "maxsmith"}
    ]
    # Adding dummy users
    for user in dummy_users:
        dynamodb.add_user(email=user["email"], password=user["password"], username=user["username"])

    dummy_shops = [
        {"shop_name": "John Micro", "email": "micro@example.com", "password": "password11",
         "address": "Hoferstrasse 19, Zuerich", "phone": "+41 1234567890"},
        {"shop_name": "Jane Hydro", "email": "hydro@example.com", "password": "password22",
         "address": "Bernerstrasse 18, Bern", "phone": "+41 2395678901"},
        {"shop_name": "Max Electro", "email": "electro@example.com", "password": "password33",
         "address": "Weinhofstrasse 123, Luzern", "phone": "+41 3456789012"}
    ]
    # Adding dummy shops
    for shop in dummy_shops:
        dynamodb.add_shop(shop_name=shop["shop_name"], email=shop["email"], password=shop["password"], address=shop["address"],
                 phone=shop["phone"])
