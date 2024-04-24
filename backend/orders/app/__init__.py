from flask import Flask, jsonify, request
from app import dynamodb_users, dummydata, initialise_dynamo, dynamodb_po
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    dynamodb_users.create_orders_table()
    dynamodb_po.create_product_owner_orders_table()
  #  dummydata.add_dummy_data()
    initialise_dynamo.create_s3_bucket()
    CORS(app)
    return app

app = create_app()

