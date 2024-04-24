from flask import Flask, jsonify, request
from app import dynamodb, dummydata, s3
from flask_cors import CORS
from app import dynamodb, dummydata
import logging
from app.routes import route_blueprint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def create_app():
    app = Flask(__name__)
    app.register_blueprint(route_blueprint)
    CORS(app)
    return app

app = create_app()

from app import routes

with app.app_context():
    dynamodb.create_user_management_tables()
    dummydata.add_dummy_data()
    dynamodb.create_s3_bucket()
    s3.create_bucket('profilepictures')
    s3.create_bucket('shoppictures')