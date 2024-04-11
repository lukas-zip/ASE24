from flask import jsonify, request
from app import app, dynamodb
from werkzeug.utils import secure_filename
import os
import re
from botocore.exceptions import ClientError


# Test if endpoint is available
@app.route('/test', methods=['GET'])
def test():
    # Return success response
    # app.logger.info('Info level log')
    print("Hello, world!")
    return jsonify({'status': True, 'value': 'Test successful'}), 201


@app.route('/<entity>', methods=['POST'])
def register_entity(entity):
    try:
        data = request.json
        if entity == 'users':
            return register_user(data)
        elif entity == 'shops':
            return register_shop(data)
        else:
            return jsonify({'status': False, 'message': 'Invalid action'}), 400
    except ClientError as e:
        print(f"Error: {e}")
        return jsonify({'status': False, 'message': f'An error occurred'}), 500


# User registration by retrieving data from post request and saving into dynamodb
def register_user(data):
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password or not username:
        return jsonify({'status': False, 'message': 'Email, username and password are required!'}), 400
    # Check if the email is in the right format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({'status': False, 'message': 'Invalid email format!'}), 400

    try:
        new_user = dynamodb.add_user(email, password, username, address, phone)
        if new_user is None:
            return jsonify({'status': False, 'message': 'Unable to register the user. E-Mail address may already be in use.'}), 400
        return jsonify({'status': True, 'value': new_user}), 200

    except ClientError as e:
        print("Error adding user:", e)
        return jsonify({'status': False, 'message': 'An error occurred while registering the user'}), 500

# Shop registration by retrieving data from post request and saving into dynamodb
def register_shop(data):
    email = data.get('email')
    shop_name = data.get('shop_name')
    description = data.get('description')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not shop_name or not password:
        return jsonify({'status': False, 'message': 'Email, shop name, address and password are required!'}), 400
    # Check if the email is in the right format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({'status': False, 'message': 'Invalid email format!'}), 400

    try:
        new_shop = dynamodb.add_shop(shop_name, email, password, address, phone, description)
        if new_shop is None:
            return jsonify({'status': False, 'message': 'Unable to register the shop. E-Mail address may already be in use.'}), 400
        return jsonify({'status': True, 'value': new_shop}), 200

    except ClientError as e:
        print("Error adding user:", e)
        return jsonify({'status': False, 'message': 'An error occurred while registering the shop'}), 500


# Check if user already  exists and provide login to platform
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': False, 'message': 'Email and password are required'}), 400

    try:
        # Check if entity exists and password is correct
        login = dynamodb.check_login(email, password)
        if login:
            return jsonify({'status': True, 'value': login}), 200
        else:
            return jsonify({'status': False, 'message': 'Invalid login credentials'}), 401
    except ClientError as e:
        return jsonify({'status': False, 'message': str(e)}), 500


@app.route('/<entity>/<entity_uuid>', methods=['PUT'])
def update_entity(entity, entity_uuid):
    try:
        if 'file' in request.files:
            file = request.files['file']
            return update_picture(file, entity_uuid)
        data = request.json
        action = data.get('action')
        if entity == 'users' and action == 'update':
            return update_user(data, entity_uuid)
        elif entity == 'shops' and action == 'update':
            return update_shop(data, entity_uuid)
        elif action == 'password':
            return change_password(data, entity_uuid)
        else:
            jsonify({'status': False, 'message': 'Invalid action'}), 400
    except ClientError as e:
        print(f"Error deleting {entity_uuid}: {e}")
        return jsonify({'status': False, 'message': f'An error occurred'}), 500


# Update function for shop
def update_shop(data, entity_uuid):
    # Retrieve the data sent in the request
    shop_name = data.get('shop_name')
    description = data.get('description')
    email = data.get('email')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not shop_name:
        return jsonify({'status': False, 'message': 'Email and shop name cannot be empty!'}), 400

    # Check if the email is in the right format
    if email:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return jsonify({'status': False, 'message': 'Invalid email format!'}), 400


    attributes = {
        'email': email,
        'shop_name': shop_name,
        'description': description,
        'address': address,
        'phone': phone
    }

    try:
        update_response = dynamodb.update_entity(entity_uuid, attributes)
        if update_response:
            return jsonify({'status': True, 'value': update_response}), 200
        else:
            return jsonify({'status': False, 'message': 'Failed to update shop'}), 400
    except ClientError as e:
        print(f"Error updating shop: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while updating the shop'}), 500


def update_user(data, entity_uuid):
    # Retrieve the data sent in the request
    email = data.get('email')
    username = data.get('username')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not username:
        return jsonify({'status': False, 'message': 'Email and username cannot be empty!'}), 400

    # Check if the email is in the right format
    if email:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return jsonify({'status': False, 'message': 'Invalid email format!'}), 400

    attributes = {
        'email': email,
        'username': username,
        'address': address,
        'phone': phone
    }

    try:
        update_response = dynamodb.update_entity(entity_uuid, attributes)
        if update_response:
            return jsonify({'status': True, 'value': update_response}), 200
        else:
            return jsonify({'status': False, 'message': 'Failed to update user'}), 400
    except ClientError as e:
        print(f"Error updating user: {e}")
        return jsonify({'status': False, 'message': 'An error occurred while updating the user'}), 500


def change_password(data, entity_uuid):
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'status': False, 'error': 'Missing old or new password'}), 400

    try:
        response = dynamodb.change_password(entity_uuid, old_password, new_password)
        if response == "mismatch":
            return jsonify({'status': False, 'message': 'The old password is incorrect.'}), 401
        elif response:
            return jsonify({'status': True, 'value': response}), 401
        else:
            return jsonify({'status': False, 'message': 'An error occurred while changing the password. Please try again!'}), 401
    except ClientError as e:
        return jsonify({'status': False, 'message': str(e)}), 500


def update_picture(file, entity_uuid):
    if file.filename == '':
        return jsonify({'status': False, 'message': 'No selected file'}), 400

    allowed = {'png', 'jpg', 'jpeg'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed):
        return jsonify({'status': False, 'message': 'File format not supported'}), 400

    if file:
        # Secure the filename and prepend "profile" to it
        filename = secure_filename(file.filename)
        _, extension = os.path.splitext(filename)
        new_filename = f"profile_picture{extension}"
        # Set up the upload folder
        upload_folder = './profilepictures'
        os.makedirs(upload_folder, exist_ok=True)
        # Construct the full file path
        file_path = os.path.join(upload_folder, new_filename)
        # Save the file locally
        file.save(file_path)
        profile_picture_url = dynamodb.update_profile_picture(entity_uuid, file_path, new_filename)
        os.remove(file_path)

        jsonify({'status': True, 'value': 'File uploaded successfully', 'url': profile_picture_url}), 200

        response = dynamodb.get_entity_json(entity_uuid)
        if not response:
            return jsonify({'status': False, 'message': 'No entity or failed to retrieve it'}), 400
        return jsonify({'status': True, 'value': response}), 201
    return jsonify({'status': False, 'message': 'File uploaded unsuccessfull'}), 401


@app.route('/<entity>/<entity_uuid>', methods=['GET'])
def get_entity(entity, entity_uuid):
    try:
        if entity == 'users':
            response = dynamodb.get_user_json(dynamodb.get_user(entity_uuid))
        elif entity == 'shops':
            response = dynamodb.get_shop_json(dynamodb.get_shop(entity_uuid))
        else:
            return jsonify({'status': False, 'message': 'Invalid entity'}), 400

        if not response:
            return jsonify({'status': False, 'message': 'No entity or failed to retrieve it'}), 400
        return jsonify({'status': True, 'value': response}), 201
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'status': False, 'message': 'An error occurred while fetching the entity.'}), 500


@app.route('/<entity>/<entity_uuid>', methods=['DELETE'])
def delete_entity(entity, entity_uuid):
    try:
        if entity == 'users':
            response = dynamodb.delete_user(entity_uuid)
        elif entity == 'shops':
            response = dynamodb.delete_shop(entity_uuid)
        else:
            return jsonify({'status': False, 'message': 'Invalid entity'}), 400

        if response:
            return jsonify({'status': True, 'value': f'Deleted successfully'}), 200
        else:
            return jsonify({'status': False, 'message': f'No entity or failed to delete'}), 400
    except ClientError as e:
        print(f"Error deleting {entity_uuid}: {e}")
        return jsonify({'status': False, 'message': f'An error occurred while deleting the {entity_uuid}'}), 500
