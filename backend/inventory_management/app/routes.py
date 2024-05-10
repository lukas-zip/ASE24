from flask import jsonify, Blueprint, request
from flask_cors import CORS
from app import dynamodb, s3
from botocore.exceptions import ClientError
from io import BytesIO
from urllib.parse import quote_plus
#from app.routes import route_blueprint

route_blueprint = Blueprint('', __name__,)

# ------------------------------------------
# For destination check
# ------------------------------------------
@route_blueprint.route('/', methods=['GET'])
def test():
    """
    Test endpoint for inventory management.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes a success message and a status indicator.
            HTTP status code is 200 (OK).

    Routes:
        GET /

    Raises:
        None
    """

    # Return success response
    return jsonify({'value': 'Test was successful for the inventorymanagement', 'status': True}), 200

@route_blueprint.route('/productsbyowner', methods=['GET'])
def get_products_by_owner():
    """
    Retrieves products by owner from DynamoDB and returns them as JSON. Mainly used for Dummy Data.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes a list of products with their details.
            HTTP status code is 200 (OK).

    Routes:
        GET /productsbyowner

    Raises:
        Any exceptions raised during DynamoDB operation or internal errors.
    """
    # Retrieve products by owner from DynamoDB
    products = dynamodb.get_products_by_product_owner("1324a686-c8b1-4c84-bbd6-17325209d78c6")

    # Format the products into a list of dictionaries
    final_products = [{
            'product_id': product_id,
            **product_info
        } for product_id, product_info in products.items()]

    # Check if products are found
    if final_products:
        # Return JSON response with products and status True
        return jsonify({'value': final_products, 'status': True}), 200
    else:
        # Return empty list with status True
        return jsonify({'value':[], 'status': True}), 200

# ------------------------------------------


# ------------------------------------------
# Shop functions
# ------------------------------------------
# product insertion function
@route_blueprint.route('/product/insert', methods=['POST'])
def insert_product():
    """
    Inserts a product into the database and returns a status JSON response.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes a status message indicating success or failure.
            HTTP status code is 200 (OK) if successful, 400 (Bad Request) or 500 (Internal Server Error) otherwise.

    Routes:
        POST /product/insert

    Raises:
        ClientError: If there is an error while adding the product to the database.
    """
    # Get JSON data from request
    data = request.json
    
    # Extract form data
    product_owner = data.get('product_owner')
    product_name = data.get('product_name')
    product_description = data.get('product_description')
    product_current_stock = data.get('product_current_stock')
    product_should_stock = data.get('product_should_stock')
    product_price = data.get('product_price')
    product_picture = data.get('product_picture')
    product_price_reduction = data.get('product_price_reduction')
    product_sale = data.get('product_sale')
    product_category = data.get('product_category')
    product_search_attributes = data.get('product_search_attributes')
    product_reviews = data.get('product_reviews')
    product_bom = data.get('product_bom')
    product_assemblies = data.get('product_assemblies')

    # Check if any required fields are missing
    if None in (product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_category, product_search_attributes, product_reviews, product_bom, product_assemblies):
        return jsonify({'error': "All values need to at least contain one value.", 'status': False}), 400

    # Validate data types
    if type(product_owner) != str or type(product_name) != str or type(product_description) != str or type(product_current_stock) != int or type(product_should_stock) != int or type(product_price) != float or type(product_picture) != list or type(product_price_reduction) != float or type(product_sale) != bool or type(product_category) != list or type(product_search_attributes) != list or type(product_reviews) != list or type(product_bom) != list or type(product_assemblies) != str:
        return jsonify({'error': "All values should need to be in expected dataformat.", 'status': False}), 400

    # Check for negative numeric values
    if product_current_stock < 0 or product_should_stock < 0 or product_price < 0 or product_price_reduction < 0:
        return jsonify({'error': "The numeric values are not allowed to be negative.", 'status': False}), 400

    # Add the product to the database
    try:
        dynamodb.add_product(product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_search_attributes, product_reviews, product_bom, product_assemblies, product_picture)
        return jsonify({'value': 'Product inserted successfully.', 'status': True}), 200
    except ClientError as e:
        print("Error adding product:", e)
        return jsonify({'error': 'Failed to insert product.', 'status': False}), 500


@route_blueprint.route('/product/upload/picture', methods = ['POST'])
def upload_picture():

    """
    Uploads a product picture to S3 and returns the URL.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes the uploaded image URL and a status message.
            HTTP status code is 200 (OK) if successful, 400 (Bad Request) or 500 (Internal Server Error) otherwise.

    Routes:
        POST /product/upload/picture

    Raises:
        ClientError: If there is an error while uploading the image to S3.
    """

    # introducing productpicture bucket
    bucket_name = 'productpictures'
    allowed_mime_types = ['image/jpeg', 'image/jpg', 'image/png', 'video/mp4']

    # Check if the request contains form data
    if 'image' not in request.files:
        return 'No image file provided', 400

    # Get the image file
    image_file = request.files['image']

    # Check if the image filename is empty
    if image_file.filename == '':
        return 'No selected file', 400

    object_key = image_file.filename
    object_type = image_file.mimetype

    if object_type not in allowed_mime_types:
        return jsonify({'error': "The dataformat cannot be accepted.", 'status': False}), 400

    #Convert bytes object to file-like object
    image_stream = BytesIO(image_file.read())

    #Construct the URL/path to the uploaded image
    s3_base_url = f'http://localhost:4566/{bucket_name}/' # Der Link ist derzeit auf Local angepasst
    image_url = s3_base_url + quote_plus(object_key)

    try:
        # Upload the image file to S3
        s3response = s3.upload_fileobj(image_stream, bucket_name, object_key)
        #print("Product picture added with UUID:", product_uuid)
        if s3response:
            return jsonify({'value': image_url, 'status': True}), 200
        else:
            return jsonify({'value': 'The image could unfortunately not be inserted', 'status': False}), 500
    except ClientError as e:
        print("Error uploading product picture to S3:", e)
        return

    #object_key = f'{product_uuid}.jpg'  # Use UUID as object key

# product deletion
@route_blueprint.route('/product/delete', methods=['DELETE'])
def delete_product_haendler():

    """
    Handles the deletion of a product.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes a status message indicating success or failure.
            HTTP status code is 200 (OK) if successful, 400 (Bad Request) or 500 (Internal Server Error) otherwise.

    Routes:
        DELETE /product/delete

    Raises:
        ClientError: If there is an error while deleting the product from the database or S3.
    """

    data = request.json
    product_id = data.get('product_id')

    # Check if product exists
    try:
        if dynamodb.product_check(product_id):
            # Commit final deletion
            product_data = dynamodb.get_product(product_id)
            for picture_path in product_data.get('product_picture', []):
                s3_object_key = picture_path.split('/')[-1]  # Extract object key from the picture path
                deletion_response = s3.delete_object(s3_object_key)
                if deletion_response:
                    print(f"Product picture '{s3_object_key}' deleted successfully from S3.")
                else:
                    print(f"Error deleting product picture '{s3_object_key}' from S3.")

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
@route_blueprint.route('/product/sell/<product_id>', methods=['PUT'])
def product_sell(product_id):

    """
    Handles selling of a product.

    Parameters:
        product_id (str): The ID of the product to be sold.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes a status message indicating success or failure.
            HTTP status code is 200 (OK) if successful, 400 (Bad Request) or 500 (Internal Server Error) otherwise.

    Routes:
        PUT /product/sell/<product_id>

    Raises:
        ClientError: If there is an error while performing the sell operation.
    """

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

# ------------------------------------------
# Consumer functions
# ------------------------------------------

# get certain product, used when clicking on a product --> product view
@route_blueprint.route('/product/<product_id>', methods=['GET'])
def get_product_info(product_id):

    """
    Retrieves information about a product.

    Parameters:
        product_id (str): The ID of the product to retrieve information for.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes the product information and a status message.
            HTTP status code is 200 (OK) if successful, 400 (Bad Request) or 500 (Internal Server Error) otherwise.

    Routes:
        GET /product/<product_id>

    Raises:
        ClientError: If there is an error while retrieving the product information.
    """

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
@route_blueprint.route('/product/cataloguesell/<product_owner>', methods=['GET'])
def get_products_to_sell_catalog(product_owner):

    """
    Retrieves products to be sold from a catalog.

    Parameters:
        product_owner (str): The owner of the products to retrieve.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes the products to sell and a status message.
            HTTP status code is 200 (OK) if successful, or 500 (Internal Server Error) otherwise.

    Routes:
        GET /product/cataloguesell/<product_owner>

    Raises:
        ClientError: If there is an error while retrieving the products.
    """

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
@route_blueprint.route('/product/cataloguebuild/<product_owner>', methods=['GET'])
def get_products_to_build_catalog(product_owner):

    """
    Retrieves products for building from a catalog.

    Parameters:
        product_owner (str): The owner of the products to retrieve.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes the products to build and a status message.
            HTTP status code is 200 (OK) if successful, or 500 (Internal Server Error) otherwise.

    Routes:
        GET /product/cataloguebuild/<product_owner>

    Raises:
        ClientError: If there is an error while retrieving the products.
    """

    try:
        products = dynamodb.get_products_by_product_owner(str(product_owner))
        final_products = [{
            'product_id': product_id,
            **product_info
        } for product_id, product_info in products.items() if product_info.get('product_assemblies') == 'Secondary']
        if final_products:
            return jsonify({'value': final_products, 'status': True}), 200
        else:
            return jsonify({'value': final_products, 'status': True}), 200
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.', 'status': False}), 500

@route_blueprint.route('/product/update_product/<product_id>', methods=['PUT'])
def update_product_route(product_id):

    """
    Updates product information.

    Parameters:
        product_id (str): The ID of the product to update.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes a status message indicating success or failure.
            HTTP status code is 200 (OK) if successful, or 500 (Internal Server Error) otherwise.

    Routes:
        PUT /product/update_product/<product_id>

    Raises:
        Any exceptions that occur during the update process.
    """

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
@route_blueprint.route('/product/search', methods=['GET'])
def search():

    """
    Performs a search for products.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes the search results and a status message.
            HTTP status code is 200 (OK) if successful, or 400 (Bad Request) otherwise.

    Routes:
        GET /product/search

    Raises:
        None
    """

    term = request.args.get('term')
    if not term:
        return jsonify({'error': 'Search term parameter is required', 'status': False}), 400
    
    #Perform search by category and attributes
    print("Searching products by category for term:", term)
    products_by_category = dynamodb.search_products_by_category(term)
    print("Products by category:", products_by_category)
    
    print("Searching products by attributes for term:", term)
    products_by_attributes = dynamodb.search_products_by_attributes(term)
    print("Products by attributes:", products_by_attributes)

    # Combine and return the results
    combined_results = {**products_by_category, **products_by_attributes}
    
    #implementation of what if products have search attribute and category matching
    formatted_results = [product_info for _, product_info in combined_results.items()]

    return jsonify({'value': formatted_results, 'status': True}), 200

@route_blueprint.route('/product/category', methods=['GET'])
def get_category():

    """
    Retrieves products by category.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes the products matching the category and a status message.
            HTTP status code is 200 (OK) if successful, or 400 (Bad Request) otherwise.

    Routes:
        GET /product/category

    Raises:
        None
    """

    category = request.args.get('term')
    if not category:
        return jsonify({'error': 'Search category parameter is required', 'status': False}), 400
    
    # Perform search by category and attributes
    print("Searching products by category for term:", category)
    products_by_category = dynamodb.search_products_by_category(category)
    print("Products by category:", products_by_category)
    
    formatted_results = [product_info for _, product_info in products_by_category.items()]

    return jsonify({'value': formatted_results, 'status': True}), 200

@route_blueprint.route('/product/production/fullfilled/<product_id>', methods=['PUT'])
def set_production(product_id):

    """
    Sets production for a product.

    Parameters:
        product_id (str): The ID of the product for which production is being set.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes a status message indicating success or failure.
            HTTP status code is 200 (OK) if successful, or 400 (Bad Request) or 500 (Internal Server Error) otherwise.

    Routes:
        PUT /product/production/fullfilled/<product_id>

    Raises:
        Any exceptions that occur during the process.
    """
    
    data = request.json

    if not isinstance(data['amount'], int) or data['amount'] < 1:
        return jsonify({'error': 'The product seems not to exist', 'status': False}), 400

    try:
        response = dynamodb.product_check(product_id)
        if response:
            item = dynamodb.get_product(product_id)
            current_stock = item['product_current_stock']

            new_stock = int(current_stock) + data['amount']

            # setting new update dict
            update_data = {'product_current_stock': new_stock}

            #update
            db_insertion = dynamodb.update_product(product_id, item['product_owner'], update_data)
            if db_insertion:
                return jsonify({'value': 'The production products have been inserted.', 'status': True}), 200
            else:
                return jsonify({'error': 'The production products, could not be inserted.', 'status': False}), 400
        else:
            return jsonify({'error': 'The product seems not to exist', 'status': False}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'status': False}), 500

# this function aims to respond with all products by a product owner that should be restocked (case: current_stock <= should_stock)
@route_blueprint.route('/product/production/recommendations/<product_owner>', methods=['GET'])
def get_production_recommendations(product_owner):

    """
    Retrieves production recommendations for a product owner.

    Parameters:
        product_owner (str): The owner of the products to retrieve production recommendations for.

    Returns:
        tuple: A tuple containing JSON response and HTTP status code.
            JSON response includes the production recommendations and a status message.
            HTTP status code is 200 (OK) if successful, or 500 (Internal Server Error) otherwise.

    Routes:
        GET /product/production/recommendations/<product_owner>

    Raises:
        ClientError: If there is an error while retrieving the production recommendations.
    """
    
    try:
        products = dynamodb.get_products_by_product_owner(str(product_owner))

        production_products = [{
            'product_id': product_id,
            **product_info
        } for product_id, product_info in products.items() if int(product_info.get('product_current_stock')) <= int(product_info.get('product_should_stock'))]

        if production_products:
            return jsonify({'value': production_products, 'status': True}), 200
        else:
            return jsonify({'value': production_products, 'status': True}), 200
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.', 'status': False}), 500
