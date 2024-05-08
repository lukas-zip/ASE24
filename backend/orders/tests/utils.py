import requests
import json

def get_all_products():
    url = f"http://inventory_management:8002/product"
    response = requests.get(url)
    products = json.loads(response.content.decode('utf-8'))['value']
    return products