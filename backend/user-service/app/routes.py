from flask import jsonify, request
from app import app, dynamodb
from werkzeug.utils import secure_filename
import os
from botocore.exceptions import ClientError


# Test if endpoint is available
@app.route('/', methods=['GET'])
def test():
    # Return success response
    #app.logger.info('Info level log')
    print("Hello, world!")
    return jsonify({'message': 'Test successful'}), 201


# User registration by retrieving data from post request and saving into dynamodb
@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password or not username:
        return jsonify({'error': 'Email, username and password are required!'}), 400

    try:
        return dynamodb.add_user(email, password, username, address, phone), 200
    except ClientError as e:
        print("Error adding user:", e)


@app.route('/user/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    # Retrieve the data sent in the request
    data = request.json
    email = data.get('email')
    username = data.get('username')
    address = data.get('address')
    phone = data.get('phone')
    new_password = data.get('new_password')

    # In case no update information is provided
    if not email and not username and not address and not phone:
        return jsonify({'error': 'No update information provided!'}), 400

    attributes = {
        'email': email,
        'username': username,
        'address': address,
        'phone': phone
    }

    try:
        # Update user details by calling the function for the database
        if new_password:
            update_response = dynamodb.update_entity(user_id, attributes, new_password)
        else:
            update_response = dynamodb.update_entity(user_id, attributes)
        if update_response:
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 400
    except ClientError as e:
        print(f"Error updating user: {e}")
        return jsonify({'error': 'An error occurred while updating the user'}), 500


# Shop registration by retrieving data from post request and saving into dynamodb
@app.route('/shop/register', methods=['POST'])
def register_shop():
    data = request.json
    email = data.get('email')
    shop_name = data.get('shop_name')
    description = data.get('description')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not shop_name or not address or not password:
        return jsonify({'error': 'Email, shop name, address and password are required!'}), 400
    try:
        return dynamodb.add_shop(shop_name, email, password, address, phone, description), 200
    except ClientError as e:
        print("Error adding user:", e)


# Update function for shops
@app.route('/shop/update/<shop_id>', methods=['PUT'])
def update_shop(shop_id):
    # Retrieve the data sent in the request
    data = request.json
    shop_name = data.get('shop_name')
    description = data.get('description')
    email = data.get('email')
    address = data.get('address')
    phone = data.get('phone')
    new_password = data.get('new_password')

    # In case no update information is provided
    if not shop_name and not description and not email and not address and not phone:
        return jsonify({'error': 'No update information provided!'}), 400

    attributes = {
        'email': email,
        'shop_name': shop_name,
        'description': description,
        'address': address,
        'phone': phone
    }

    try:
        # Update user details by calling the function for the database
        if new_password:
            update_response = dynamodb.update_entity(shop_id, attributes, new_password)
        else:
            update_response = dynamodb.update_entity(shop_id, attributes)
        if update_response:
            return jsonify({'message': 'Shop updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update shop'}), 400
    except ClientError as e:
        print(f"Error updating shop: {e}")
        return jsonify({'error': 'An error occurred while updating the shop'}), 500


# Check if user already  exists and provide login to platform
@app.route('/login', methods=['POST'])
def login():
    # Retrieve data from post request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        # Check if entity exists and password is correct
        if dynamodb.check_password(email, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid login credentials'}), 401
    except ClientError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/profilepicture/<entity_uuid>', methods=['POST'])
def update_picture(entity_uuid):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    allowed = {'png', 'jpg', 'jpeg'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed):
        return jsonify({'error': 'File format not supported'}), 400

    if file:
        # Secure the filename and prepend "profile" to it
        filename = secure_filename(file.filename)
        _, extension = os.path.splitext(filename)
        new_filename = f"profile_picture{extension}"
        # Set up the upload folder
        upload_folder = './backend/user-service'
        os.makedirs(upload_folder, exist_ok=True)
        # Construct the full file path
        file_path = os.path.join(upload_folder, new_filename)
        # Save the file locally
        file.save(file_path)
        profile_picture_url = dynamodb.update_profile_picture(entity_uuid, file_path, new_filename)
        os.remove(file_path)
        return jsonify({'message': 'File uploaded successfully', 'url': profile_picture_url}), 200
    return jsonify({'message': 'File uploaded unsuccessfull'}), 401


@app.route('/delete/<entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    try:
        response = dynamodb.delete_entity(entity_id)
        if response:
            return jsonify({'message': f'{entity_id} deleted successfully'}), 200
        else:
            return jsonify({'error': f'Failed to delete {entity_id}'}), 400
    except ClientError as e:
        print(f"Error deleting {entity_id}: {e}")
        return jsonify({'error': f'An error occurred while deleting the {entity_id}'}), 500





