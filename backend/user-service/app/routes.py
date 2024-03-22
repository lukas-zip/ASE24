from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from app import app, dynamodb
import uuid
from botocore.exceptions import ClientError


@app.route('/', methods=['GET'])
def test():
    # Return success response
    return jsonify({'message': 'Test successful'}), 201


@app.route('/user/create', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        return dynamodb.add_user(email, password, username), 200
    except ClientError as e:
        print("Error adding user:", e)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        entity = dynamodb.user_in_db(email)

        # Check if entity exists and password is correct
        if entity and (entity['password'], password):
            return jsonify({'message': 'Login successful', 'type': entity['Type']}), 200
        else:
            return jsonify({'error': 'Invalid login credentials'}), 401
    except ClientError as e:
        return jsonify({'error': str(e)}), 500
