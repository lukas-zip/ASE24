import requests
import json
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
import urllib.request

def get_product_details(product_id):
    url = "http://localhost:8002/product/"+product_id
    url = "http://localstack:4566/product"
    
    response = requests.get(url)

    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    # session.get(url, verify=False)

   # product = urllib.request.urlopen(url).read()

    return response.content

def calc_discounted_price(price, discount):
    return (price - (float(price) * float(discount) / 100))
