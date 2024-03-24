from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from app import app, dynamodb
import uuid
from botocore.exceptions import ClientError

# @app.route('/user/create', methods=['POST'])
# def create_user():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({'error': 'Email and password are required'}), 400
#     try:
#         # Check if the user already exists
#         if dynamodb.get_user_by_email(email):
#             print(f"User with email {email} already exists")
#             return

#         # Generate UUID for the new user
#         user_uuid = str(uuid.uuid4())

#         # Put the new item into the table
#         dynamodb.db_users.put_item(
#             TableName='UserProfiles',
#             Item={
#                 'profile_id': {'S': user_uuid},  # Automatically generated UUID
#                 'email': {'S': email},  # User's email address
#                 'password': {'S': password}  # User's password (should be hashed in production)
#             }
#         )
#         print("User added with UUID:", user_uuid)
#         return jsonify({'success': 'Yayy'}), 200
#     except ClientError as e:
#         print("Error adding user:", e)


@app.route('/', methods=['GET'])
def test():
    # Return success response
    return jsonify({'message': 'Test was successful for the inventorymanagement'}), 201

@app.route('/productsbyowner', methods=['GET'])
def get_products_by_owner():
    # Retrieve products by owner
    products = dynamodb.get_products_by_product_owner("999999999")

    if products:
        return jsonify(products), 200
    else:
        return jsonify([]), 200



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
