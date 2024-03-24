from flask import Flask, jsonify, request
from app import dynamodb
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    dynamodb.create_product_table()
    dynamodb.create_product_owner_index()
    dynamodb.add_dummy_products()
    CORS(app)
    return app

app = create_app()

