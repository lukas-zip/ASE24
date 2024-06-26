import json
import time

from app import dynamodb


def add_dummy_data():
    time.sleep(2)
    with open("dummydata/products.json", "r") as f:
        dummy_products = json.load(f)
    i = 0
    for p in dummy_products:
        dynamodb.add_product(
            product_owner=p["product_owner"],
            product_name=p["product_name"],
            product_description=p["product_description"],
            product_current_stock=p["product_current_stock"],
            product_should_stock=p["product_should_stock"],
            product_price=p["product_price"],
            product_price_reduction=p["product_price_reduction"],
            product_sale=p["product_sale"],
            product_category=p["product_category"],
            product_search_attributes=p["product_search_attributes"],
            product_reviews=p["product_reviews"],
            product_bom=p["product_bom"],
            product_assemblies=p["product_assemblies"],
            product_picture=p["product_picture"],
            product_uuid="product_id_test" + str(i),
        )
        i += 1
