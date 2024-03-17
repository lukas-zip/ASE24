from flask import Flask, jsonify, request
from app import dynamodb
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    dynamodb.create_profiles_table()
    dynamodb.create_email_index()
    dynamodb.add_dummy_users()
    CORS(app)
    return app

app = create_app()

