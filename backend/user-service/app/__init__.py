from flask import Flask, jsonify, request
from app import dynamodb, dummydata, s3
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    dynamodb.create_user_management_tables()
    #dummydata.add_dummy_data()
    #dynamodb.create_s3_bucket()
    s3.create_bucket('profilepictures')
    s3.create_bucket('shoppictures')
    CORS(app)
    return app

app = create_app()