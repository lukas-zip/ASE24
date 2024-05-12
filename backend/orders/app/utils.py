import json

import requests

# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# import urllib.request


def get_product_details(product_id):
    """Get product details from inventory management service

    Args:
        product_id (string): Product ID

    Returns:
        : product price, discount percentage and product owner name/ID
    """
    url = f"http://inventory_management:8002/product/{product_id}"
    response = requests.get(url)
    product_details = json.loads(response.content.decode("utf-8"))["value"]

    # get product details
    product_price_reduction = float(product_details["product_price_reduction"])
    product_price = float(product_details["product_price"])
    product_owner = product_details["product_owner"]

    return product_price, product_price_reduction, product_owner


def get_all_product_details(product_id):
    """Get product details from inventory management service

    Args:
        product_id (string): Product ID

    Returns:
        : json of all product info
    """
    url = f"http://inventory_management:8002/product/{product_id}"
    response = requests.get(url)
    product_details = json.loads(response.content.decode("utf-8"))["value"]
    return product_details


def calc_discounted_price(price, discount):
    """Calculate product price after discount

    Args:
        price : product price
        discount : product discount

    Returns:
        float: product price after discount
    """
    return price - (float(price) * float(discount) / 100)


def reformat_order_reponse(item):
    """Reformats order form DynamoDB format that includes object type, to a more readable format

    Args:
        item : DynamoDB item

    Returns:
        json: Reformatted json
    """
    orders_arr = []
    orders_dict = {}
    product_owners_dict = {}

    orders = item.get("orders", {}).get("M", [])
    product_owners = item.get("product_owners", {}).get("M", [])

    # return orders
    for key, value in orders.items():
        product_details = get_all_product_details(key)
        orders_arr.append(
            {
                "product_id": key,
                "quantity": float(value["N"]),
                "product_owner": product_owners[key]["S"],
                "price": float(product_details["product_price"]),
                "price_reduction": float(product_details["product_price_reduction"]),
                "final_price": calc_discounted_price(
                    float(product_details["product_price"]),
                    float(product_details["product_price_reduction"]),
                ),
            }
        )

    for order in orders.keys():
        orders_dict[order] = orders[order].get("N", "")

    for po in product_owners.keys():
        product_owners_dict[po] = product_owners[po].get("S", "")

    return {
        "order_id": item.get("order_id", {}).get("S", ""),
        "orders_fe": orders_arr,
        "orders": orders_dict,
        "product_owners": product_owners_dict,
        "total_price": item.get("total_price", {}).get("N", ""),
        "user_id": item.get("user_id", {}).get("S", ""),
        "execution_time": item.get("execution_time", {}).get("S", ""),
        "order_status": item.get("order_status", {}).get("S", ""),
    }


def reformat_po_order_reponse(item):
    """Reformats PO order form DynamoDB format that includes object type, to a more readable format

    Args:
        item : DynamoDB item

    Returns:
        json: Reformatted json
    """
    orders_dict = {}
    orders = item.get("orders", {}).get("M", [])

    po_orders_arr = []
    # return orders
    for key, value in orders.items():
        po_orders_arr.append(
            {
                "product_id": key,
                "quantity": float(value["N"]),
                "product_details": get_all_product_details(key),
            }
        )

    for order in orders.keys():
        orders_dict[order] = orders[order].get("N", "")

    return {
        "po_order_id": item.get("po_order_id", {}).get("S", ""),
        "execution_time": item.get("execution_time", {}).get("S", ""),
        "order_id": item.get("order_id", {}).get("S", ""),
        "orders": orders_dict,
        "order_status": item.get("order_status", {}).get("S", ""),
        "total_price": item.get("total_price", {}).get("N", ""),
        "product_owner": item.get("product_owner", {}).get("S", ""),
        "user_id": item.get("user_id", {}).get("S", ""),
        "orders_fe": po_orders_arr,
    }


def reformat_order_arr_reponse(response):
    """Reformats an array of user orders form DynamoDB format that includes object type, to a more readable format

    Args:
        response : DynamoDB reponse

    Returns:
        json: Reformatted json
    """
    items = response.get("Items")
    final_res = []
    for item in items:
        final_res.append(reformat_order_reponse(item))

    return {"Count": response.get("Count"), "Items": final_res}


def reformat_po_order_arr_reponse(response):
    """Reformats an array of PO orders form DynamoDB format that includes object type, to a more readable format

    Args:
        response : DynamoDB reponse

    Returns:
        json: Reformatted json
    """
    items = response.get("Items")
    final_res = []
    for item in items:
        final_res.append(reformat_po_order_reponse(item))

    return {"Count": response.get("Count"), "Items": final_res}
