from flask import Flask, jsonify, request
from app import dynamodb_users,dynamodb_po , invoice,initialise_dynamo
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    dynamodb_users.create_orders_table()
    dynamodb_po.create_product_owner_orders_table()
    initialise_dynamo.create_s3_bucket()
    invoice.create_s3_bucket()
    CORS(app)
    return app

app = create_app()

