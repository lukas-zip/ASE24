import requests
import json

def get_total_cost(orders):
    url = "https://localhost:8002/product/"
    total_price =  0 
    for product_id in order:
        response = requests.post(url+product_id, json=data, headers=headers)
        product = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        total_price += product.price
    return total_price
