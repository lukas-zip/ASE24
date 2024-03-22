from flask import Flask, jsonify, request
from app import dynamodb
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    dynamodb.create_user_management_tables()
    dynamodb.add_dummy_data()
    CORS(app)
    return app

app = create_app()

