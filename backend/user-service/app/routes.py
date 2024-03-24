from flask import Flask, jsonify, request, send_file
from app import app, dynamodb
from werkzeug.utils import secure_filename
import os
from botocore.exceptions import ClientError

# Test if endpoint is available
@app.route('/t2', methods=['GET'])
def test():
    # Return success response
    app.logger.info('Info level log')
    print("Hello, world!")
    return jsonify({'message': 'Test successful'}), 201

# User registration by retrieving data from post request and saving into dynamodb
@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        return jsonify({'error': 'Email, username and password are required!'}), 400

    try:
        return dynamodb.add_user(email, password, username), 200
    except ClientError as e:
        print("Error adding user:", e)

# Shop registration by retrieving data from post request and saving into dynamodb
@app.route('/shop/register', methods=['POST'])
def register_shop():
    data = request.json
    email = data.get('email')
    shop_name = data.get('shop_name')
    address = data.get('address')
    phone = data.get('phone')
    password = data.get('password')

    if not email or not shop_name or not address or not phone or not password:
        return jsonify({'error': 'Please provide all registration details!'}), 400

    try:
        return dynamodb.add_shop(shop_name, email, password, address, phone), 200
    except ClientError as e:
        print("Error adding user:", e)

# Check if user already  exists and provide login to platform
@app.route('/user', methods=['POST'])
def login():
    # Retrieve data from post request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        entity = dynamodb.user_in_db(email)
        # Check if entity exists and password is correct
        if entity and (entity['password'], password):
            return jsonify({'message': 'Login successful', 'type': entity['type']}), 200
        else:
            return jsonify({'error': 'Invalid login credentials'}), 401
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/profile/<entity_uuid>', methods=['POST'])
def update_profile_picture(entity_uuid):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

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


@app.route('/user/<user_uuid>', methods=['POST'])
def test_user(user_uuid):
    test = dynamodb.get_user(user_uuid)
    return jsonify({'error': 'No file part', 'Entity': test}), 200