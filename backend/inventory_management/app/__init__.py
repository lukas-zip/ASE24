from flask import Flask, jsonify, request
from app import dynamodb, s3, dummydata_products
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    dynamodb.create_product_table()
    dynamodb.create_product_owner_index()
    s3.create_bucket()
    dynamodb.create_gsi()
    #dummydata_products.insert_dummy_products()
    #dynamodb.insert_dummy_products()
    #dummy_data.insert_dummy_products()
    #dynamodb.add_dummy_products()
    dummydata_products.add_dummy_data()
    #dummydata_products.insert_product()
    CORS(app)
    return app

app = create_app()

