from flask import jsonify
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

user_ids = []
shop_ids = []
product_ids = []
order_ids = []


def create_user_shop(data, type):
    if type == 'User':
        url = "http://user-service:8001/users"
    else:
        url = "http://user-service:8001/shops"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        data = response.json()
        if type == 'User':
            entity_id = data['value']['user_id']
        else:
            entity_id = data['value']['shop_id']
        return entity_id
    else:
        return None


def create_product(data):
    url = "http://inventory_management:8002/product/insert"
    files = {'image': open('pictures/image.png', 'rb')}
    # Send POST request
    response = requests.post(url, data=data, files=files)
    if response.status_code == 200:
        data = response.json()
        product_id = data['value']
        return product_id
    else:
        return None


def create_order(data):
    url = "http://orders:8004/orders"
    response = requests.post(url, data=data)
    if response.status_code == 200:
        data = response.json()
        order_id = data['value']
        return order_id
    else:
        return None


def add_dummy_data():
    #add users to the plattform
    with open('data/users.json', 'r') as f:
        dummy_users = json.load(f)
        for user in dummy_users:
            user_ids.append(create_user_shop(user, 'User'))
    #add shops to the plattform
    with open('data/shops.json', 'r') as f:
        dummy_shops = json.load(f)
        for shop in dummy_shops:
            shop_ids.append(create_user_shop(shop, 'Shop'))
    with open('data/products.json', 'r') as f:
        dummy_products = json.load(f)
        for product in dummy_products:
            product['product_owner'] = shop_ids[0]
            product_ids.append(create_product(product))
    #with open('data/shops.json', 'r') as f:
     #   dummy_orders = json.load(f)
      #  for order in dummy_orders:
       #     order['username'] = user_ids[0]
            #order['orders'] = (x for x in product_ids)
          #  order_ids.append(create_order(order))


add_dummy_data()