from flask import Flask, request, jsonify
from flask_cors import CORS
from app import app, dynamodb_po, dynamodb_users, invoice
from werkzeug.utils import secure_filename
import os
import re
from botocore.exceptions import ClientError
from datetime import datetime, date
from types import SimpleNamespace
import json
from app import utils

app.config["DEBUG"] = True

# Test if endpoint is available
@app.route('/', methods=['GET'])
def test():
    # Return success response
    print("Hello, world!")
    return jsonify({'status': True, 'message': 'Test successful'}), 201



@app.get("/orders/<order_id>")
def get_order_req(order_id):
    response = dynamodb_users.get_order(order_id)
    return jsonify(response), 201


@app.get("/orders")
def get_all_orders_req():
    response = dynamodb_users.get_all_orders()
    return jsonify(response), 201


@app.delete("/orders/<order_id>")
def delete_order_req(order_id: int):
    res = dynamodb_users.delete_order(order_id)
    return jsonify(res), 201


@app.put("/orders/<order_id>")
def update_order_req(order_id):
    data = request.json
    res = dynamodb_users.update_order(order_id, data['product_id'], data['quantity'])
    return jsonify(res), 201



@app.get("/orders/users/search/<user_id>")
def search_orders(user_id):
    data = request.json
    res = dynamodb_users.search_orders(user_id)
    return jsonify(res), 201


@app.post("/orders")
def add_order_req():
    data = request.json
    
    if data['quantity'] <= 0:
        return jsonify({'error': 'order quantity should be at least 1', 'status': False}), 400
    res = dynamodb_users.add_item(data['user_id'],data['product_id'], data['quantity'])
    return jsonify(res), 201


@app.get("/orders/product/search/<product_owner_id>")
def search_po_orders(product_owner_id):
    res = dynamodb_po.search_orders_by_po(product_owner_id) 
    return jsonify(res), 201

@app.get("/orders/product/<order_id>/<product_owner_id>/delivered")
def set_po_orders_delivered(order_id, product_owner_id):
    res = dynamodb_po.update_po_status(product_owner_id, order_id,'delivered')
    return jsonify(res), 201

@app.get("/orders/product/<order_id>/<product_owner_id>/shipped")
def set_po_orders_shipped(order_id, product_owner_id):
    res = dynamodb_po.update_po_status(product_owner_id, order_id,'shipped')
    return jsonify(res), 201


# Create a invoice pdf out of the order details for one order
@app.route('/invoice/<order_id>', methods=['POST'])
def route_create_invoice(order_id):
    if not order_id:
        return jsonify({'error': 'ID is required!'}), 400
    try:
        message, status = invoice.create_pdf(order_id)
        if status == True:
            return jsonify({'value': message,'status': status}), 200
        else:
            return jsonify({'message': message,'status': status}), 200
    except ClientError as e:
        print("Error adding review:", e)

## Download the invoice for a specific order
@app.route('/invoice/<order_id>',methods=['GET'])
def route_get_invoice(order_id):
    if not order_id:
        return jsonify({'error': 'ID is required!'}), 400
    try:
        item, status = invoice.get_invoice(order_id)
        return jsonify({'value': item,'status': status}), 200     
    except ClientError as e:
        print("Error adding review:", e)
        return jsonify({'error': 'Failed to get review'}), 500


# ----------------------------------------------------------------------------#
# Testing APIs
# ----------------------------------------------------------------------------#

@app.get("/orders/test/<product_id>")
def test_orders(product_id):
    res = utils.get_product_details(product_id)
    return res, 201

@app.get("/orders/po")
def get_all_po_orders():
    response = dynamodb_po.get_all_po_orders()
    return jsonify(response), 201

@app.get("/orders/po/test/search/order_id/<order_id>")
def search_po_orders_orderid(order_id):
    response = dynamodb_po.search_orders_by_orderid(order_id)
    return jsonify(response), 201

@app.get("/orders/test/po/search/<order_id>/<product_owner_id>")
def test_search_po_orders(order_id,product_owner_id):
    response = dynamodb_po.search_po_orders(product_owner=product_owner_id, order_id=order_id)
    return jsonify(response), 201



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