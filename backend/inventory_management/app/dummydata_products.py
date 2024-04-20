from app import dynamodb
import json
import time

def add_dummy_data():
    time.sleep(2)
    with open('dummydata/products.json', 'r') as f:
        dummy_products = json.load(f)
    for p in dummy_products:
        dynamodb.add_product(product_owner=p['product_owner'], product_name=p['product_name'], product_description=p['product_description'], product_current_stock=p['product_current_stock'], product_should_stock=p['product_should_stock'], product_price=p['product_price'], product_price_reduction=p['product_price_reduction'], product_sale=p['product_sale'], product_category=p['product_category'], product_search_attributes=p['product_search_attributes'], product_reviews=p['product_reviews'], product_bom=p['product_bom'], product_assemblies=p['product_assemblies'], product_picture=p['product_picture'])


    # with open('dummydata/shops.json', 'r') as f:
    #     dummy_shops = json.load(f)
    # for shop in dummy_shops:
    #     dynamodb.add_shop(shop_name=shop["shop_name"], description=shop["description"], email=shop["email"], password=shop["password"],
    #                       address=shop["address"], phone=shop["phone"])