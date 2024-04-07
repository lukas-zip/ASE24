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
    return jsonify({'value': 'Test was successful for the inventorymanagement', 'status': True}), 201

@app.route('/productsbyowner', methods=['GET'])
def get_products_by_owner():
    # Retrieve products by owner
    products = dynamodb.get_products_by_product_owner("1324a686-c8b1-4c84-bbd6-17325209d78c6")

    final_products = [{
            'product_id': product_id,
            **product_info
        } for product_id, product_info in products.items()]

    if final_products:
        return jsonify({'value': final_products, 'status': True}), 200
    else:
        return jsonify({'value':[], 'status': True}), 200
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
    if not all([product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_search_attributes, product_assemblies]):
        return jsonify({'error': 'Product data is incomplete.', 'status': False}), 400

    # Check if the image filename is empty
    if image_file.filename == '':
        return 'No selected file', 400

    # Dont know if we want to ask for different other criteria

    # Add the product to the database
    try:
        dynamodb.add_product(product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_search_attributes, product_reviews, product_bom, product_assemblies, image_file)
        return jsonify({'value': 'Product inserted successfully.', 'status': True}), 200
    except ClientError as e:
        print("Error adding product:", e)
        return jsonify({'error': 'Failed to insert product.', 'status': False}), 500

# product deletion
@app.route('/product/delete', methods=['DELETE'])
def delete_product_haendler():
    data = request.json
    product_id = data.get('product_id')

    # Check if product exists
    try:
        if dynamodb.product_check(product_id):
            # Commit final deletion
            response = dynamodb.delete_product(product_id)
            if response:
                return jsonify({'value': 'The item got deleted from the database.', 'status': True}), 200
            else:
                return jsonify({'error': 'An error occurred while deleting the item.', 'status': False}), 500
        else:
            # Return that the product cannot be deleted since it does not exist
            return jsonify({'error': 'Product does not exist.', 'status': False}), 400
    except ClientError as e:
        print("Error deleting product:", e)
        return jsonify({'error': 'An error occurred while processing your request.', 'status': False}), 500

# process a sell --> providing the ID for the sell of the product
@app.route('/product/sell/<product_id>', methods=['PUT'])
def product_sell(product_id):
    try:
        data = request.json
    
        # Ensure product_id and product_owner are provided in the request body
        if 'product_owner' not in data:
            return jsonify({'error': 'product_owner is required in the request body', 'status': False}), 400
        if 'amount' not in data:
            return jsonify({'error': 'amount is required in the request body', 'status': False}), 400

        response = dynamodb.perform_sell(product_id, data['product_owner'], data['amount'])
        if response:
            return jsonify({'value': 'successfully performed sell.', 'status': True}), 200
        else:
            return jsonify({'error': 'unsuccessful sell', 'status': False}), 400
    except ClientError as e:
        return jsonify({'error': str(e), 'status': False}), 500





# production recommendations
# update product







# ------------------------------------------
# Consumer functions
# ------------------------------------------

# get certain product, used when clicking on a product --> product view
@app.route('/product/<product_id>', methods=['GET'])
def get_product_info(product_id):
    try:
        product_info = dynamodb.get_product(str(product_id))
        if product_info:
            return jsonify({'value': product_info, 'status': True}), 200
        else:
            return jsonify({'error': 'The Item does not exist', 'status': False}), 400
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.', 'status': False}), 500

# get product catalogue for a certain seller --> used to show all products belonging to one seller
@app.route('/product/cataloguesell/<product_owner>', methods=['GET'])
def get_products_to_sell_catalog(product_owner):
    try:
        products = dynamodb.get_products_by_product_owner(str(product_owner))
        final_products = [{
            'product_id': product_id,
            **product_info
        } for product_id, product_info in products.items() if product_info.get('product_assemblies') == 'Final']
        if final_products:
            return jsonify({'value': final_products, 'status': True}), 200
        else:
            return jsonify({'value': final_products, 'status': True}), 200
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.', 'status': False}), 500
    
# get product catalogue for a certain seller --> shows all products that secondary
@app.route('/product/cataloguebuild/<product_owner>', methods=['GET'])
def get_products_to_build_catalog(product_owner):
    try:
        products = dynamodb.get_products_by_product_owner(str(product_owner))
        final_products = [{
            'product_id': product_id,
            **product_info
        } for product_id, product_info in products.items() if product_info.get('product_assemblies') == 'Secondary']
        if final_products:
            return jsonify({'value': final_products, 'status': True}), 200
        else:
            return jsonify({'error': 'no items available for this product_owner', 'status': False}), 400
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.', 'status': False}), 500

@app.route('/product/update_product/<product_id>', methods=['PUT'])
def update_product_route(product_id):
    try:
        # Get the updated product data from the request
        updated_data = request.json
        
        # Ensure product_id and product_owner are provided in the request body
        if 'product_owner' not in updated_data:
            return jsonify({'error': 'product_owner is required in the request body', 'status': False}), 400
        
        # Call the update_product function to perform the update
        success = dynamodb.update_product(product_id, updated_data['product_owner'], updated_data)
        
        if success:
            return jsonify({'value': 'Product updated successfully', 'status': True}), 200
        else:
            return jsonify({'error': 'Failed to update product', 'status': False}), 500
    except Exception as e:
        return jsonify({'error': str(e), 'status': False}), 500

# Define search route
@app.route('/product/search', methods=['GET'])
def search():
    term = request.args.get('term')
    if not term:
        return jsonify({'error': 'Search term parameter is required', 'status': False}), 400
    
    # Perform search by category and attributes
    print("Searching products by category for term:", term)
    products_by_category = dynamodb.search_products_by_category(term)
    print("Products by category:", products_by_category)
    

    print("Searching products by attributes for term:", term)
    products_by_attributes = dynamodb.search_products_by_attributes(term)
    print("Products by attributes:", products_by_attributes)
    
 

    # Combine and return the results
    combined_results = {**products_by_category, **products_by_attributes}
    
    formatted_results = [product_info for _, product_info in combined_results.items()]

    return jsonify({'value': formatted_results, 'status': True}), 200

@app.route('/product/category', methods=['GET'])
def get_category():
    category = request.args.get('term')
    if not category:
        return jsonify({'error': 'Search category parameter is required', 'status': False}), 400
    
    # Perform search by category and attributes
    print("Searching products by category for term:", category)
    products_by_category = dynamodb.search_products_by_category(category)
    print("Products by category:", products_by_category)
    
    formatted_results = [product_info for _, product_info in products_by_category.items()]

    return jsonify({'value': formatted_results, 'status': True}), 200




# we need a administrative view that states which attributes are available