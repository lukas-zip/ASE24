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


def reformat_reponse(response):
    item = response.get('Item')
    return {
                'execution_time': item.get('execution_time', {}).get('S', ''),
                'order_id': item.get('order_id', {}).get('S', ''),
                'orders': item.get('orders', {}).get('SS', []),
                'quantities': item.get('quantities', {}).get('NS', []),
                'status': item.get('status', {}).get('S', ''),
                'total_price': item.get('total_price', {}).get('N', ''),
                'username': item.get('username', {}).get('S', '')
            }