from flask import Flask, jsonify, request
from app import dynamodb, dummydata, invoice
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    dynamodb.create_orders_table()
    dummydata.add_dummy_data()
    dynamodb.create_s3_bucket()
    invoice.create_s3_bucket()
    CORS(app)
    return app

app = create_app()

