from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from app import app, dynamodb
import uuid
from botocore.exceptions import ClientError

# Test if endpoint is available
@app.route('/', methods=['GET'])
def test():
    # Return success response
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
