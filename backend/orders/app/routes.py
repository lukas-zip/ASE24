from flask import Flask, request, jsonify
from flask_cors import CORS
from app import app, dynamodb
from werkzeug.utils import secure_filename
import os
import re
from botocore.exceptions import ClientError
from datetime import datetime, date
from types import SimpleNamespace
import json

#app = Flask(__name__)
app.config["DEBUG"] = True
#CORS(app)


# class Product():
#     product_id int
#     company_id int
#     category str
#     price int
#     quantity_in_stock int 
#     product_rating int 
#     created_at datetime

# class Order():
#     products: list[Product]
#     total_price: int 
#     status: str
#     executed: datetime

# Test if endpoint is available
@app.route('/', methods=['GET'])
def test():
    # Return success response
    print("Hello, world!")
    return jsonify({'status': True, 'message': 'Test successful'}), 201


@app.get("/orders/{order_id}")
def get_order(order_id):
    orders = get_order(order_id)
    return jsonify('sss'), 201


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    res = delete_order(order_id)
    return jsonify(res), 201


#update order (remove/add product)
# {
#     "product": product_id1",
#     "action": 'add' / 'remove',
# }
@app.put("/orders/{order_id}")
def update_order(order_id: int):
    data = request.json
    data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    print(order_id, data.product ,data.action)
    res = update_order(order_id, data.product ,data.action)
    return jsonify(res), 201


# add new order
# {
#     "product": product_id1"
# }
# @app.post("/orders/{order_id} ")
def add_order(order_id: int):
    data = request.json
    data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    print(order_id, data.product)
    res = update_order(order_id, data.product)
    return jsonify(res), 201

# ----------------------------------------------------------------------------#
# Error Handling.
# ----------------------------------------------------------------------------#

@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }, 405)


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }, 500)