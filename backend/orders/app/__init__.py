import logging

from app import dynamodb_po, dynamodb_users, initialise_dynamo, invoice
from app.routes import route_blueprint
from flask import Flask, jsonify, request
from flask_cors import CORS

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


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
