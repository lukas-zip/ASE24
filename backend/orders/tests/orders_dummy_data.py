from tests.product_dummy_data import get_product_dummy_data
from tests.utils import calc_discounted_price


def get_orders_dummy_data(inp_orders_id):
    """examples of json that should be returned by the orders service in different test cases

    Args:
        inp_orders_id : order id

    Returns:
        json : order json
    """

    # create order
    order_id = "order_id1"
    user_id = "user_id1"
    order_status = "unpaid"
    quantity = 3
    product_id = "product_id1"
    product_data = get_product_dummy_data(product_id)
    po = product_data["product_owner"]
    price = product_data["product_price"]
    product_price_reduction = product_data["product_price_reduction"]
    total_price = calc_discounted_price(price, product_price_reduction)

    data1 = {
        "execution_time": "2024-05-10 06:24:34.842174",
        "order_id": f"{order_id}",
        "order_status": f"{order_status}",
        "orders": {f"{product_id}": f"{quantity}"},
        "product_owners": {f"{product_id}": f"{po}"},
        "total_price": f"{total_price}",
        "user_id": f"{user_id}",
    }
    if order_id == inp_orders_id:
        return data1

    # update
    product_id = "product_id2"
    po = "po_id1"
    product_name = "product 2"
    product_price = 500
    product_price_reduction = 5
    data2 = {
        "product_assemblies": "Final",
        "product_bom": ["UUID1"],
        "product_category": ["Necless"],
        "product_current_stock": "10",
        "product_description": "Description of Product Y",
        "product_id": f"{product_id}",
        "product_name": f"{product_name}",
        "product_owner": f"{po}",
        "product_picture": [
            "http://localhost:4566/productpictures/thisexampleproduct.png"
        ],
        "product_price": f"{product_price}",
        "product_price_reduction": f"{product_price_reduction}",
        "product_reviews": [""],
        "product_sale": False,
        "product_search_attributes": ["Greenish", "Platin"],
        "product_shoulproduct_price = " "d_stock": "20",
    }
    if product_id == inp_product_id:
        return data2

    product_id = "product_id3"
    po = "po_id2"
    product_name = "product 3"
    product_price = 1000
    product_price_reduction = 10
    data3 = {
        "product_assemblies": "Final",
        "product_bom": ["UUID1"],
        "product_category": ["Necless"],
        "product_current_stock": "10",
        "product_description": "Description of Product Y",
        "product_id": f"{product_id}",
        "product_name": f"{product_name}",
        "product_owner": f"{po}",
        "product_picture": [
            "http://localhost:4566/productpictures/thisexampleproduct.png"
        ],
        "product_price": f"{product_price}",
        "product_price_reduction": f"{product_price_reduction}",
        "product_reviews": [""],
        "product_sale": False,
        "product_search_attributes": ["Greenish", "Platin"],
        "product_shoulproduct_price = " "d_stock": "20",
    }
    if product_id == inp_product_id:
        return data3

    product_id = "product_id4"
    po = "po_id2"
    product_name = "product 4"
    product_price = 300
    product_price_reduction = 30
    data4 = {
        "product_assemblies": "Final",
        "product_bom": ["UUID1"],
        "product_category": ["Necless"],
        "product_current_stock": "10",
        "product_description": "Description of Product Y",
        "product_id": f"{product_id}",
        "product_name": f"{product_name}",
        "product_owner": f"{po}",
        "product_picture": [
            "http://localhost:4566/productpictures/thisexampleproduct.png"
        ],
        "product_price": f"{product_price}",
        "product_price_reduction": f"{product_price_reduction}",
        "product_reviews": [""],
        "product_sale": False,
        "product_search_attributes": ["Greenish", "Platin"],
        "product_shoulproduct_price = " "d_stock": "20",
    }
    if product_id == inp_product_id:
        return data4

    product_id = "product_id4"
    po = "po_id2"
    product_name = "product 4"
    product_price = 300
    product_price_reduction = 30
    data4 = {
        "product_assemblies": "Final",
        "product_bom": ["UUID1"],
        "product_category": ["Necless"],
        "product_current_stock": "10",
        "product_description": "Description of Product Y",
        "product_id": f"{product_id}",
        "product_name": f"{product_name}",
        "product_owner": f"{po}",
        "product_picture": [
            "http://localhost:4566/productpictures/thisexampleproduct.png"
        ],
        "product_price": f"{product_price}",
        "product_price_reduction": f"{product_price_reduction}",
        "product_reviews": [""],
        "product_sale": False,
        "product_search_attributes": ["Greenish", "Platin"],
        "product_shoulproduct_price = " "d_stock": "20",
    }
    if product_id == inp_product_id:
        return data4
