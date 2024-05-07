from flask import Flask, jsonify, request
from app import dynamodb_users,dynamodb_po , invoice,initialise_dynamo
from flask_cors import CORS
from app.routes import route_blueprint
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# def create_app():
#     app = Flask(__name__)
#     dynamodb_users.create_orders_table()
#     dynamodb_po.create_product_owner_orders_table()
#     initialise_dynamo.create_s3_bucket()
#     invoice.create_s3_bucket()
#     CORS(app)
#     return app

# app = create_app()



def create_app():
    app = Flask(__name__)
    app.register_blueprint(route_blueprint)
    CORS(app)
    return app

app = create_app()

with app.app_context():
    dynamodb_users.create_orders_table()
    dynamodb_po.create_product_owner_orders_table()
    initialise_dynamo.create_s3_bucket()
    invoice.create_s3_bucket()