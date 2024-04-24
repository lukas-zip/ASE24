import requests
import json
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
import urllib.request

def get_product_details(product_id):
    url = f"http://inventory_management:8002/product/{product_id}"
    response = requests.get(url)
    print('CAALING INVENTORYYY')
    print(json.loads(response.content.decode('utf-8')))
    product_details = json.loads(response.content.decode('utf-8'))['value']
 
    #get product details
    product_price_reduction = float(product_details['product_price_reduction'])
    product_price = float(product_details['product_price'])
    product_owner = product_details['product_owner']

    return product_price, product_price_reduction, product_owner

def calc_discounted_price(price, discount):
    return (price - (float(price) * float(discount) / 100))

def reformat_order_reponse(item):
    orders_arr =[]
    orders_dict = {}
    product_owners_dict = {}

    orders = item.get('orders', {}).get('M', [])
    product_owners = item.get('product_owners', {}).get('M', [])
    
   # return orders
    for key, value in orders.items():
        orders_arr.append({ "product_id":key , "quantity" : int(value['N']) , "product_owner": product_owners[key]['S']})

    for order in orders.keys():
        orders_dict[order] = orders[order].get('N', '')

    for po in product_owners.keys():
        product_owners_dict[po] = product_owners[po].get('S', '')

    
    return {
                'order_id': item.get('order_id', {}).get('S', ''),
                'orders_fe': orders_arr,
                'orders': orders_dict,
                'product_owners': product_owners_dict,
                'total_price': item.get('total_price', {}).get('N', ''),
                'user_id': item.get('user_id', {}).get('S', '')
          }

def reformat_po_order_reponse(item):
    orders_dict = {}
    orders = item.get('orders', {}).get('M', [])

    for order in orders.keys():
        orders_dict[order] = orders[order].get('N', '')

    return {
                'po_order_id': item.get('po_order_id', {}).get('S', ''),
                'execution_time': item.get('execution_time', {}).get('S', ''),
                'order_id': item.get('order_id', {}).get('S', ''),
                'orders': orders_dict,
                'order_status': item.get('order_status', {}).get('S', ''),
                'total_price': item.get('total_price', {}).get('N', ''),
                'order_status': item.get('order_status', {}).get('S', ''),
                'product_owner': item.get('product_owner', {}).get('S', ''),
                'user_id': item.get('user_id', {}).get('S', '')
          }


def reformat_order_arr_reponse(response):
    items = response.get('Items')
    final_res = []
    for item in items:
        final_res.append(reformat_order_reponse(item))

    return  {"Count":response.get('Count'), "Items":final_res}


def reformat_po_order_arr_reponse(response):
    items = response.get('Items')
    final_res = []
    for item in items:
        final_res.append(reformat_po_order_reponse(item))

    return  {"Count":response.get('Count'), "Items":final_res}

