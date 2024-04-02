from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import boto3
from app import app, dynamodb, s3
import uuid
from botocore.exceptions import ClientError
from io import BytesIO
import base64

# ------------------------------------------
# For destination check
# ------------------------------------------
@app.route('/', methods=['GET'])
def test():
    # Return success response
    return jsonify({'message': 'Test was successful for the inventorymanagement'}), 201

@app.route('/productsbyowner', methods=['GET'])
def get_products_by_owner():
    # Retrieve products by owner
    products = dynamodb.get_products_by_product_owner("1324a686-c8b1-4c84-bbd6-17325209d78c6")

    if products:
        return jsonify(products), 200
    else:
        return jsonify([]), 200
# ------------------------------------------


# ------------------------------------------
# Shop functions
# ------------------------------------------
# product insertion function
@app.route('/product/insert', methods=['POST'])
def insert_product():
    # Check if the request contains form data
    if 'image' not in request.files:
        return 'No image file provided', 400
    
    # Get form data
    product_owner = request.form.get('product_owner')
    product_name = request.form.get('product_name')
    product_description = request.form.get('product_description')
    product_current_stock = request.form.get('product_current_stock')
    product_should_stock = request.form.get('product_should_stock')
    product_price = request.form.get('product_price')
    product_price_reduction = request.form.get('product_price_reduction')
    product_sale = request.form.get('product_sale')
    product_category = request.form.getlist('product_category')  # Use getlist() for multiple values
    product_search_attributes = request.form.getlist('product_search_attributes')  # Use getlist() for multiple values
    product_reviews = request.form.getlist('product_reviews')  # Use getlist() for multiple values
    product_bom = request.form.getlist('product_bom')
    product_assemblies = request.form.get('product_assemblies')

    # Get the image file
    image_file = request.files['image']
    
    # Checking for required fields
    if not all([product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_search_attributes, product_reviews, product_bom, product_assemblies]):
        return jsonify({'error': 'Product data is incomplete.'}), 400

    # Check if the image filename is empty
    if image_file.filename == '':
        return 'No selected file', 400

    # Dont know if we want to ask for different other criteria

    # Add the product to the database
    try:
        dynamodb.add_product(product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_search_attributes, product_reviews, product_bom, product_assemblies, image_file)
        return jsonify({'success': 'Product inserted successfully.'}), 200
    except ClientError as e:
        print("Error adding product:", e)
        return jsonify({'error': 'Failed to insert product.'}), 500

# product deletion
@app.route('/product/delete', methods=['POST'])
def delete_product_haendler():
    data = request.json
    product_id = data.get('product_id')

    # Check if product exists
    try:
        if dynamodb.product_check(product_id):
            # Commit final deletion
            response = dynamodb.delete_product(product_id)
            if response:
                return jsonify({'success': 'The item got deleted from the database.'}), 200
            else:
                return jsonify({'error': 'An error occurred while deleting the item.'}), 500
        else:
            # Return that the product cannot be deleted since it does not exist
            return jsonify({'error': 'Product does not exist.'}), 400
    except ClientError as e:
        print("Error deleting product:", e)
        return jsonify({'error': 'An error occurred while processing your request.'}), 500







# ------------------------------------------
# Consumer functions
# ------------------------------------------

# get certain product
@app.route('/product/<uuid:product_id>', methods=['GET'])
def get_product_info(product_id):
    try:
        product_info = dynamodb.get_product(str(product_id))
        if product_info:
            return jsonify(product_info=product_info), 200
        else:
            return jsonify({'error': 'The Item does not exist'}), 400
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

# get product catalogue for a certain seller
@app.route('/catalogue/<product_owner>', methods=['GET'])
def get_products_to_sell_catalog(product_owner):
    try:
        products = dynamodb.get_products_by_product_owner(str(product_owner))
        if products :
            return jsonify(products), 200
        else:
            return jsonify({'message': 'no items available for this product_owner'}), 400
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500
    



# process a sell
# process a production of certain material



    

































# #get product
# @app.route('/product/fetch/uuid', methods=['GET'])
# def fetch_product():
#     pass #for specific request

# @app.route('/product/fetch/product_owner/product_name', methods=['GET'])
# def fetch_single_product():
#     pass #for search for example contains string or partial string in name

# @app.route('/product/fetch/catalog', methods=['GET'])
# def fetch_product_catalog():
#     pass

# # update product attributes
# @app.route('/product/update/product_name', methods=['GET'])
# def update_product_name():
#     pass

# @app.route('/product/update/product_picture', methods=['GET'])
# def update_product_picture():
#     pass

# @app.route('/product/update/product_description', methods=['GET'])
# def update_product_description():
#     pass

# @app.route('/product/update/product_current_stock', methods=['GET'])
# def update_product_current_stock():
#     pass

# @app.route('/product/update/product_should_stock', methods=['GET'])
# def update_product_should_stock():
#     pass

# @app.route('/product/update/product_price', methods=['GET'])
# def update_product_price():
#     pass

# @app.route('/product/update/product_price_reduction', methods=['GET'])
# def update_product_price_reduction():
#     pass

# @app.route('/product/update/product_sale', methods=['GET'])
# def update_product_sale():
#     pass

# @app.route('/product/update/product_category', methods=['GET'])
# def update_product_category():
#     pass

# @app.route('/product/update/product_search_attributes', methods=['GET'])
# def update_product_search_attributes():
#     pass

# @app.route('/product/update/product_reviews', methods=['GET'])
# def update_product_reviews():
#     pass

# @app.route('/product/update/product_bom', methods=['GET'])
# def update_product_bom():
#     pass

# @app.route('/product/update/product_assemblies', methods=['GET'])
# def update_product_assemblies():
#     pass



# @app.route('/user/login', methods=['POST'])
# def login():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({'error': 'Email and password are required'}), 400

#     user = dynamodb.get_user_by_email(email)
#     # print(jsonify(user))
#     if user:
#         stored_password = user.get('password', {}).get('S')
#         print("Stored password:", stored_password)
#         print("Password provided by user:", password)
#         if stored_password == password:
#             return jsonify({'message': 'Login successful'}), 200
#     return jsonify({'error': 'Incorrect email or password'}), 401
