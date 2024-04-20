import requests
import json
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
import urllib.request

def get_product_details(product_id):
    url = f"http://inventory_management:8002/product/{product_id}"

#    requests.get(f"http://orders:8004/orders/{order_id}")
    
    response = requests.get(url)

    # session = requests.Session()
    # retry = Remtry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    # session.get(url, verify=False)

   # product = urllib.request.urlopen(url).read()
    
    return json.loads(response.content.decode('utf-8'))['value']

def calc_discounted_price(price, discount):
    return (price - (float(price) * float(discount) / 100))


def reformat_reponse(item):
    orders_dict ={}
    orders = item.get('orders', {}).get('M', [])

    for order in orders.keys():
        orders_dict[order] = orders[order].get('N', '')

    return {
                'execution_time': item.get('execution_time', {}).get('S', ''),
                'order_id': item.get('order_id', {}).get('S', ''),
                'orders': orders_dict,
                'order_status': item.get('order_status', {}).get('S', ''),
                'total_price': item.get('total_price', {}).get('N', ''),
                'order_status': item.get('order_status', {}).get('S', ''),
                'product_owner': item.get('product_owner', {}).get('S', ''),
                'user_id': item.get('user_id', {}).get('S', '')
          }