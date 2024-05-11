def get_orders_dummy_data(inp_product_id):

    product_id = "product_id1"
    po = "po_id1"
    product_name = "product 1"
    product_price = 100
    product_price_reduction = 10
    data1 = {
        "execution_time": "2024-05-10 06:24:34.842174",
        "order_id": "db5ddd76-9396-4ebe-a62c-46ae71b4aa33",
        "order_status": "unpaid",
        "orders": {"61363bc2-0aba-4d0f-aa84-4e4af17086b6": "7"},
        "orders_fe": [
            {
                "final_price": 90.0,
                "price": 100.0,
                "price_reduction": 10.0,
                "product_id": "61363bc2-0aba-4d0f-aa84-4e4af17086b6",
                "product_owner": "1324a686-c8b1-4c84-bbd6-17325209d78c6",
                "quantity": 7.0,
            }
        ],
        "product_owners": {
            "61363bc2-0aba-4d0f-aa84-4e4af17086b6": "1324a686-c8b1-4c84-bbd6-17325209d78c6"
        },
        "total_price": "630",
        "user_id": "username_test3",
    }
    if product_id == inp_product_id:
        return data1

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
